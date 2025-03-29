import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load RMSD data from file (replace 'rmsd_matrix.txt' with your file)
rmsd_matrix = np.loadtxt('complex_map.txt')

# Plot composite RMSD map as a heatmap using Seaborn
sns.heatmap(rmsd_matrix, cmap='viridis', cbar_kws={'label': 'RMSD (Å)'})
plt.title('Composite RMSD Map')
plt.xlabel('Frame')
plt.ylabel('Frame')
plt.savefig('rmsd_map.png', dpi=300, bbox_inches='tight')
plt.show()
