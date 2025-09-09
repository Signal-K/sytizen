import os
from astroquery.mast import Catalogs
import lightkurve as lk
import matplotlib.pyplot as plt
import random

def plot_sectors_with_temperature(star_id, bin_time_minutes=15, catalog_type="TIC"):
    """
    Create and save light curve plots for all available sectors of a given TIC/KIC ID.

    Parameters:
    - star_id: The TIC or KIC ID for which to generate plots.
    - bin_time_minutes: Time interval for binning the light curves, in minutes.
    - catalog_type: Either "TIC" or "KIC" to specify the catalog.
    """ 
    bin_time_days = bin_time_minutes / 24 / 60  # Convert minutes to days

    # Format the target name based on catalog type
    target_name = f"{catalog_type} {star_id}"
    
    # Query stellar properties
    try:
        if catalog_type == "TIC":
            star_info = Catalogs.query_object(target_name, catalog="TIC")
        else:  # KIC
            star_info = Catalogs.query_object(target_name, catalog="Kepler")
    except Exception as e:
        print(f"Error querying star information for {target_name}: {e}")
        star_info = []
    
    if len(star_info) == 0:
        print(f"Star information not found for {target_name}.")
        # Continue anyway, we can still plot without stellar properties
        temperature = 'Unknown'
        radius = 'Unknown'
    else:
        # Extract temperature and radius if available
        temperature = star_info[0]['Teff'] if 'Teff' in star_info.columns else 'Unknown'
        radius = star_info[0]['rad'] if 'rad' in star_info.columns else 'Unknown'

    # Search for light curves - get all available sectors
    search_result = lk.search_lightcurve(target_name, author="SPOC")
    
    # If SPOC doesn't have data, try other authors
    if len(search_result) == 0:
        print(f"No SPOC light curves found for {target_name}. Trying other authors...")
        search_result = lk.search_lightcurve(target_name)
    
    if len(search_result) == 0:
        print(f"No light curves found for {target_name}.")
        return

    print(f"Found light curve data for {target_name} in {len(search_result)} sector(s)")

    # Create folder structure: buckets/anomalies/TIC_ID/ or buckets/anomalies/KIC_ID/
    base_folder = "anomalies"
    star_folder = f"{catalog_type}_{star_id}" if catalog_type == "KIC" else str(star_id)
    output_folder = os.path.join(base_folder, star_folder)
    os.makedirs(output_folder, exist_ok=True)

    colors = ['red', 'blue', 'green', 'purple', 'orange', 'pink', 'cyan', 'magenta', 'yellow', 'brown']

    # Generate and save plots for each sector
    sector_counter = 1
    total_sectors = len(search_result)
    print(f"Found {total_sectors} sectors for {target_name}")
    
    for lc_file in search_result:
        try:
            lc = lc_file.download()
            lc = lc.remove_outliers(sigma=5)
            
            # Increase binning for simpler visualization (fewer data points)
            increased_bin_time = bin_time_days * 3  # Triple the binning time for fewer points
            lc_binned = lc.bin(increased_bin_time)

            color = colors[sector_counter % len(colors)] if sector_counter <= len(colors) else "#" + ''.join(random.choices('0123456789ABCDEF', k=6))

            # Create figure with transparent background
            plt.figure(figsize=(10, 5))
            fig = plt.gcf()
            fig.patch.set_facecolor('white')
            fig.patch.set_alpha(0.7)  # Semi-transparent background
            
            ax = plt.gca()
            ax.patch.set_facecolor('white')
            ax.patch.set_alpha(0.7)  # Semi-transparent plot area
            
            # Plot with fewer, moderately-sized markers for simpler visualization
            lc_binned.plot(marker='o', linewidth=0, color=color, alpha=0.9, markersize=4, label='Binned')

            plt.title(f"{target_name} - Sector {lc.sector}\n"
                      f"Stellar Temperature: {temperature} K | Radius: {radius} R☉", 
                      fontsize=12, pad=20)
            plt.xlabel("Time [BTJD days]", fontsize=11)
            plt.ylabel("Normalized Flux", fontsize=11)
            plt.legend(framealpha=0.7)
            
            # Make grid more subtle
            plt.grid(True, alpha=0.3)

            output_file = os.path.join(output_folder, f"Sector{sector_counter}.png")
            plt.savefig(output_file, dpi=150, bbox_inches='tight', 
                       facecolor=fig.get_facecolor(), edgecolor='none', transparent=False)
            plt.close()
            print(f"Saved plot {sector_counter}/{total_sectors}: {output_file} (TESS Sector {lc.sector})")
            
        except Exception as e:
            print(f"Error processing sector {sector_counter} for {target_name}: {e}")
            
        sector_counter += 1

# List of TIC IDs to process
tic_ids = [
    258776466, 198178859, 165598669, 161687211, 273234825, 273690178,
    259238498, 122706449, 233194447, 333324340, 177697418, 455733237
]

# Optional: List of KIC IDs to process (uncomment to use)
# kic_ids = [
#     11446443, 1430163, 9947026, 6922244, 8462852
# ]

# Additional TIC IDs (uncomment to use)
# tic_ids = [
#     440801822, 345724317, 329981856, 284300833, 277039287, 269343479, 
#     263723967, 238597883, 210904767, 201175570, 169904935, 156115721, 
#     124709665, 106997505, 88863718, 65212867, 57299130, 50365310, 21720215,
# ]

# Generate plots for each TIC ID
for tic_id in tic_ids:
    print(f"\n{'='*50}")
    print(f"Processing TIC {tic_id}...")
    print(f"{'='*50}")
    plot_sectors_with_temperature(tic_id, catalog_type="TIC")

# Generate plots for each KIC ID (uncomment to use)
# for kic_id in kic_ids:
#     print(f"\n{'='*50}")
#     print(f"Processing KIC {kic_id}...")
#     print(f"{'='*50}")
#     plot_sectors_with_temperature(kic_id, catalog_type="KIC")

print(f"\n{'='*50}")
print("All processing complete!")
print(f"{'='*50}")