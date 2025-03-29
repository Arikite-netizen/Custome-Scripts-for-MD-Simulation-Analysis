import pandas as pd

# Input files
common_residues_file = "common_active_residues.csv"
pymol_script_file = "visualize_pharmacophores.pml"
pdb_file = "protein.pdb"  # Ensure this file contains the full protein structure

# Read common active residues
df = pd.read_csv(common_residues_file)

if "Residue" not in df.columns:
    raise ValueError("Error: 'Residue' column not found in CSV file. Check the file format.")

# Extract residue data
residues = df["Residue"].tolist()

# Generate PyMOL script
with open(pymol_script_file, "w") as f:
    f.write(f"""# PyMOL script to visualize common pharmacophore residues
load {pdb_file}

# Show full protein structure properly
show cartoon, all  # Show full protein folds
color white, all   # Color the full protein white
show surface, all  # Display full protein surface
set transparency, 0.3, all
""")

    # Define colors for interaction types
    f.write("""
# Define color coding
set_color pos_interaction, [1.0, 0.3, 0.3]  # Red for positive residues
set_color neg_interaction, [0.3, 0.3, 1.0]  # Blue for negative residues
set_color hydrophobic, [0.5, 1.0, 0.5]  # Green for hydrophobic residues
set_color polar, [1.0, 1.0, 0.3]  # Yellow for polar residues
set_color surface_default, [0.7, 0.7, 0.7]  # Default gray surface
""")

    # Residue categorization (based on interactions)
    pos_residues = {"ARG", "LYS", "HIS"}
    neg_residues = {"ASP", "GLU"}
    hydrophobic_residues = {"ALA", "VAL", "LEU", "ILE", "MET", "PHE", "TRP", "PRO"}
    polar_residues = {"SER", "THR", "ASN", "GLN", "TYR", "CYS"}

    for residue in residues:
        try:
            parts = residue.split(":")  # Expected format: "R:A:RES:NUM"
            chain = parts[1]
            res_name = parts[2]
            res_num = parts[3]

            # Assign colors based on residue type
            if res_name in pos_residues:
                color = "pos_interaction"
            elif res_name in neg_residues:
                color = "neg_interaction"
            elif res_name in hydrophobic_residues:
                color = "hydrophobic"
            elif res_name in polar_residues:
                color = "polar"
            else:
                color = "white"  # Default

            # PyMOL commands to highlight the residues
            f.write(f"""
select res_{res_num}, chain {chain} and resi {res_num}
color {color}, res_{res_num}
show sticks, res_{res_num}  # Show key residues as sticks
show spheres, res_{res_num}  # Show residues as spheres
label res_{res_num}, "{res_name}{res_num}"
set label_color, black, res_{res_num}
set label_size, 18, res_{res_num}
set surface_color, {color}, res_{res_num}  # Color protein surface per residue type
""")

        except Exception as e:
            print(f"Error processing residue: {residue} - {e}")

    f.write("\n# Final adjustments\n")
    f.write("zoom all\n")
    f.write("set sphere_scale, 0.7\n")  # Larger spheres for visibility
    f.write("set label_size, 20\n")  # Bigger labels
    f.write("set surface_color, surface_default, all\n")  # Default surface color (editable)

    # Ensure the entire protein backbone is visible
    f.write("""
show cartoon, all  # Ensure the full protein is visible
show lines, all  # Show backbone and side chains
set cartoon_transparency, 0.2, all
""")

print(f"Updated PyMOL script generated: {pymol_script_file}")
