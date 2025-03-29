import pandas as pd
import os
import glob

ENERGY_THRESHOLD = -1.0  # kcal/mol threshold

def extract_active_residues(mmpbsa_file):
    """
    Extract residues contributing significantly to binding free energy from an MMPBSA decomposition file.
    Handles unexpected headers and uses chunk processing for large files.
    """
    try:
        active_residues = set()

        # Open file and detect correct header line
        with open(mmpbsa_file, "r") as f:
            lines = f.readlines()

        # Find the line number where actual data starts
        start_line = None
        for i, line in enumerate(lines):
            if line.strip().startswith("Frame #"):  # Look for actual data header
                start_line = i
                break

        if start_line is None:
            print(f"Error: Could not find data start in {mmpbsa_file}")
            return set()

        # Read CSV from the detected start line
        chunk_size = 50_000  # Adjust as needed
        for chunk in pd.read_csv(
            mmpbsa_file,
            sep=",",  # Ensure CSV format is correctly interpreted
            skiprows=start_line,  # Start from the detected header
            chunksize=chunk_size,  # Process in chunks
            dtype=str,  # Read everything as a string first
            on_bad_lines="skip"  # Skip problematic lines
        ):
            # Ensure the expected columns exist
            if "Residue" not in chunk.columns or "TOTAL" not in chunk.columns:
                print(f"Warning: {mmpbsa_file} does not have 'Residue' or 'TOTAL' columns. Skipping.")
                continue

            # Convert TOTAL column to numeric (handle non-numeric values)
            chunk["TOTAL"] = pd.to_numeric(chunk["TOTAL"], errors="coerce")

            # Filter residues that contribute significantly
            chunk_active = chunk[chunk["TOTAL"] < ENERGY_THRESHOLD]["Residue"].dropna().astype(str)
            active_residues.update(chunk_active)

        return active_residues

    except Exception as e:
        print(f"Error processing {mmpbsa_file}: {e}")
        return set()

def compare_mmpbsa_files():
    """
    Compare multiple MMPBSA decomposition files in the current directory to identify common active residues.
    """
    mmpbsa_files = glob.glob("FINAL_DECOMP_MMPBSA_PB*.csv")

    if not mmpbsa_files:
        print("No MMPBSA files found.")
        return None

    print(f"Processing {len(mmpbsa_files)} files using optimized memory handling...")

    # Extract active residues from each file
    residue_sets = [extract_active_residues(f) for f in mmpbsa_files]

    # Filter out empty sets
    residue_sets = [s for s in residue_sets if s]

    if residue_sets:
        common_residues = set.intersection(*residue_sets)
        print(f"Common active residues across ligands: {common_residues}")

        # Save results
        pd.DataFrame({"Residue": list(common_residues)}).to_csv("common_active_residues.csv", index=False)
        print("Results saved to common_active_residues.csv")
        return common_residues

    return set()

# Run the analysis
common_residues = compare_mmpbsa_files()
