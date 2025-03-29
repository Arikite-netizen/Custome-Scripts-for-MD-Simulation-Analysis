import subprocess

# Define the Gnuplot script
gnuplot_script = """
reset
set terminal pngcairo enhanced font "Arial,14" size 1000,800
set output 'FEL_plot.png'

# Enable multiplot for 3D + 2D inset
set multiplot layout 1,1

# === Main 3D Free Energy Landscape Plot ===
set view 60, 120
set xlabel "PC1" rotate by 20
set ylabel "PC2" rotate by -20
set zlabel "Free Energy (kJ/mol)" rotate parallel
set pm3d
set dgrid3d 50,50
set hidden3d   # Fixes the purple outline issue
splot 'free-energy-landscape.dat' using 1:2:3 with lines title "3D Free Energy Landscape"

# === Inset: 2D Free Energy Landscape (Top-Right) ===
set size 0.35, 0.35   # Scale down the inset plot
set origin 0.6, 0.6   # Position it at the top-right corner
set view map
unset key
unset colorbox  # REMOVE GRADIENT BAR
unset ztics

# Use contours instead of pm3d to avoid purple outline issues
set pm3d map
splot 'free-energy-landscape.dat' using 1:2:3 with pm3d title ""

unset multiplot
unset output
"""

# Save the Gnuplot script to a file
with open("plot_FEL.gnu", "w") as file:
    file.write(gnuplot_script)

# Run Gnuplot using the script
try:
    subprocess.run(["gnuplot", "plot_FEL.gnu"], check=True)
    print("✅ Free Energy Landscape plot saved as 'FEL_plot.png'")
except subprocess.CalledProcessError as e:
    print("❌ Error running Gnuplot:", e)
