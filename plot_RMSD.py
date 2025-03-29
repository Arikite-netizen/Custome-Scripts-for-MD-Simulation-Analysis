import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for aesthetics
sns.set_theme(style="whitegrid")

# Load the CSV file
file_path = "COM_RMSD.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Convert specific columns to numeric and handle invalid entries
columns_to_convert = data.columns[1:]  # Assuming the first column is the X-axis
for col in columns_to_convert:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Drop rows with NaN values (optional, depending on your data)
data.dropna(inplace=True)

# Custom color palette for each column
custom_colors = {
    "Oleuropein": "red",
    "Curcumin": "darkorange",
    "Quercetin": "yellow",
    "Cyanidin": "lightblue",
    "Epigallocatechin gallate": "navy"
}

# Prepare the plot
plt.figure(figsize=(16, 10))

# Plot the moving average for each column
for col in columns_to_convert:
    # Calculate moving average with a window size of 5
    moving_avg = data[col].rolling(window=5).mean()
    plt.plot(
        data[data.columns[0]],  # X-axis values
        moving_avg,  # Y-axis values
        label=f"{col} (Moving Avg)",
        color=custom_colors[col],
        linewidth=2.5,  # Highlighted line
        alpha=0.9  # Less transparent
    )

# Add labels and a title
plt.title(
    "Moving Averages of Complex RMSDs ",
    fontsize=18,
    weight='bold',
    pad=70  # Increased padding for more space above the legend
)
plt.xlabel("Time(ns)", fontsize=14)
plt.ylabel("RMSD(nm)", fontsize=14)

# Position the legend at the top
plt.legend(
    title="Systems",
    loc='upper center',
    bbox_to_anchor=(0.5, 1.15),  # Shift the legend further up
    ncol=5,  # Arrange items in 4 columns
    fontsize=11
)

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0, 1, 0.85])  # Adjust layout to give more space for the legend and title

# Save and show the plot
plt.savefig("COMPLEX_rmsd.png", dpi=300)
plt.show()
