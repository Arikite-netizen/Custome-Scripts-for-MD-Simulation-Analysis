import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV file
file_path = "processed_data.csv"  # Replace with your actual file
data = pd.read_csv(file_path)

# Extract ligand type and docking method from "Docking" column
data["Ligand"] = data["Docking"].apply(lambda x: x.split("_")[0])  # Extracts 'ace' or 'mgo'
data["Method"] = data["Docking"].apply(lambda x: x.split("_")[1])  # Extracts 'glide' or 'ifd'

# Find the lowest (most negative) binding energy in 'ifd' per ligand
lowest_ifd_per_ligand = data[data["Method"] == "ifd"].groupby("Ligand").apply(lambda x: x.loc[x["Binding_Energy"].idxmin()])

# Set plot style
sns.set_theme(style="whitegrid")

# Define color palette
palette = {"glide": "red", "ifd": "blue"}

# Create scatter plot without using Molecule No on X-axis
plt.figure(figsize=(10, 6))

# Plot all data points
sns.scatterplot(
    data=data, x="Docking", y="Binding_Energy", hue="Method",
    palette=palette, s=120, edgecolor="black", alpha=0.7
)

# Highlight the lowest (most negative) `ifd` binding energy per ligand
for _, row in lowest_ifd_per_ligand.iterrows():
    plt.scatter(
        row["Docking"], row["Binding_Energy"], color="gold",
        edgecolor="black", s=250, label=f"Lowest {row['Ligand'].upper()} IFD", zorder=3
    )

# Labels and title
plt.xlabel("Docking Method", fontsize=14)
plt.ylabel("Binding Energy (kcal/mol)", fontsize=14)
plt.title("Binding Energy Scatter Plot (MOPAC Simulation)", fontsize=16, weight="bold")

# Show legend
plt.legend(title="Docking Method", loc="best")

# Save and display plot
plt.savefig("binding_energy_scatter_no_xaxis.png", dpi=300)
plt.show()
