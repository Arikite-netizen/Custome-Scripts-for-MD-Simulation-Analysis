import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set Seaborn style for aesthetics
sns.set_theme(style="whitegrid")

# Load the CSV file
file_path = "RMSF.csv"  # Replace with your actual file path
data = pd.read_csv(file_path)

# Convert specific columns to numeric and handle invalid entries
columns_to_convert = data.columns[1:]  # Assuming the first column is the X-axis (Residue No.)
for col in columns_to_convert:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Drop rows with NaN values (optional)
data.dropna(inplace=True)

# Custom color palette for each ligand
custom_colors = {
    "Oleuropein": "red",
    "Curcumin": "darkorange",
    "Quercetin": "yellow",
    "Cyanidin": "lightblue",
    "Epigallocatechin gallate": "navy"
}

# Prepare the plot
plt.figure(figsize=(16, 10))

# Dictionary to store peak RMSF values and residue locations
peak_rmsf = {}

# Plot the moving average for each ligand
for col in columns_to_convert:
    moving_avg = data[col].rolling(window=5).mean()

    # Find the max RMSF peak and corresponding residue number
    max_rmsf_value = moving_avg.max()
    max_rmsf_residue = data.iloc[moving_avg.idxmax(), 0]  # Residue number

    peak_rmsf[col] = (max_rmsf_residue, max_rmsf_value)

    # Plot the moving average
    plt.plot(
        data[data.columns[0]], moving_avg, label=f"{col} (Moving Avg)",
        color=custom_colors[col], linewidth=2.5, alpha=0.9
    )

    # Highlight peak with a vertical dashed line
    plt.axvline(x=max_rmsf_residue, color=custom_colors[col], linestyle="--", alpha=0.5)

    # Annotate peak value near the highest fluctuation point
    plt.text(max_rmsf_residue, max_rmsf_value + 0.02, f"{col} Peak",
             color=custom_colors[col], fontsize=12, fontweight='bold')

# Determine the **Residue No. with the highest fluctuation in the entire dataset**
highest_residue_across = max(peak_rmsf, key=lambda k: peak_rmsf[k][1])
highest_residue_number, highest_rmsf_value = peak_rmsf[highest_residue_across]

# Highlight this **global highest fluctuation site**
plt.scatter(highest_residue_number, highest_rmsf_value, color=custom_colors[highest_residue_across],
            s=250, edgecolors="black", linewidth=2, label=f"Highest Fluctuation Site: {highest_residue_across}")

# Modify X-axis to show **every 5th residue**
plt.xticks(np.arange(data.iloc[0, 0], data.iloc[-1, 0] + 1, step=5))

# Add labels and title
plt.title("Moving Averages of Complex RMSFs with Peak Highlights", fontsize=18, weight='bold', pad=70)
plt.xlabel("Residue No.", fontsize=14)
plt.ylabel("RMSF (nm)", fontsize=14)

# Position the legend at the top
plt.legend(title="Systems", loc='upper center', bbox_to_anchor=(0.5, 1.15),
           ncol=5, fontsize=11, frameon=True)

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0, 1, 0.85])

# Save and show the plot
plt.savefig("COMPLEX_rmsf_highlighted.png", dpi=300)
plt.show()
