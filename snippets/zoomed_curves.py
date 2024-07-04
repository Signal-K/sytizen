import os
import shutil
import matplotlib.pyplot as plt
import lightkurve as lk
 
# Clear the output directory
output_dir = 'output'
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

# Define the TIC
TIC = 'TIC 50365310'

# Search for lightcurve data
sector_data = lk.search_lightcurve(TIC, author='SPOC')

# Select the first 4 sectors
select_sector = sector_data[0:4]

# Download all selected sectors
lc_collection = select_sector.download_all()

# Plot individual light curves with adjustments
lc = select_sector.download_all()
fig1, ax1 = plt.subplots()
lc.plot(ax=ax1, linewidth=0, marker='.', markersize=1, color='midnightblue', alpha=0.3)
fig1.savefig(os.path.join(output_dir, 'individual_light_curves.png'))
plt.close(fig1)

# Stitch the light curves
lc_collection_stitched = lc_collection.stitch()
fig2, ax2 = plt.subplots()
lc_collection_stitched.plot(ax=ax2, linewidth=0, marker='.', markersize=1, color='midnightblue', alpha=0.3)
fig2.savefig(os.path.join(output_dir, 'stitched_light_curves.png'))
plt.close(fig2)

# Bin the light curves with a larger bin time
bin_time = 1 / 24  # 1-hour binning
lc_collection_binned = lc_collection_stitched.bin(bin_time)
fig3, ax3 = plt.subplots()
lc_collection_binned.plot(ax=ax3, linewidth=0, marker='o', markersize=4, color='red', alpha=0.7)
fig3.savefig(os.path.join(output_dir, 'binned_light_curves.png'))
plt.close(fig3)

# Plot stitched and binned light curves together with adjustments
fig4, ax4 = plt.subplots(figsize=(10, 5))
lc_collection_stitched.plot(ax=ax4, linewidth=0, marker='.', markersize=1, color='midnightblue', alpha=0.3, label='Unbinned')
lc_collection_binned.plot(ax=ax4, linewidth=0, marker='o', markersize=4, color='red', alpha=0.7, label='Binned')
ax4.legend()
fig4.savefig(os.path.join(output_dir, 'stitched_and_binned_light_curves.png'))
plt.close(fig4)

# Optional: Zoom in on a specific time range to highlight transits
fig5, ax5 = plt.subplots(figsize=(10, 5))
lc_collection_stitched.plot(ax=ax5, linewidth=0, marker='.', markersize=1, color='midnightblue', alpha=0.3, label='Unbinned')
lc_collection_binned.plot(ax=ax5, linewidth=0, marker='o', markersize=4, color='red', alpha=0.7, label='Binned')
ax5.set_xlim(lc_collection_stitched.time.min().value, lc_collection_stitched.time.min().value + 10)  # Example zoom range
ax5.legend()
fig5.savefig(os.path.join(output_dir, 'zoomed_light_curves.png'))
plt.close(fig5)

# Apply a smoothing filter to the light curve
smoothed_lc = lc_collection_stitched.flatten(window_length=301)
fig6, ax6 = plt.subplots(figsize=(10, 5))
smoothed_lc.plot(ax=ax6, linewidth=0, marker='.', markersize=1, color='midnightblue', alpha=0.3, label='Smoothed')
fig6.savefig(os.path.join(output_dir, 'smoothed_light_curves.png'))
plt.close(fig6)
