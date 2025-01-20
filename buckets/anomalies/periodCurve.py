import os
from astroquery.mast import Catalogs
import lightkurve as lk
import matplotlib.pyplot as plt
import random

def plot_sectors_with_temperature(tic_id, bin_time_minutes=15):
    """
    Create and save light curve plots for all available sectors of a given TIC ID.

    Parameters:
    - tic_id: The TIC ID for which to generate plots.
    - bin_time_minutes: Time interval for binning the light curves, in minutes.
    """
    bin_time_days = bin_time_minutes / 24 / 60  # Convert minutes to days

    # Query stellar temperature
    star_info = Catalogs.query_object(f"TIC {tic_id}", catalog="TIC")
    if len(star_info) == 0:
        print(f"Star information not found for TIC {tic_id}.")
        return
    temperature = star_info[0]['Teff'] if 'Teff' in star_info.columns else 'Unknown'

    # Search for light curves
    search_result = lk.search_lightcurve(f"TIC {tic_id}", author="SPOC")
    if len(search_result) == 0:
        print(f"No light curves found for TIC {tic_id}.")
        return

    # Create folder for the TIC ID
    output_folder = str(tic_id)
    os.makedirs(output_folder, exist_ok=True)

    colors = ['red', 'blue', 'green', 'purple', 'orange', 'pink', 'cyan', 'magenta', 'yellow', 'brown']

    # Generate and save plots for each sector
    image_counter = 1
    for lc_file in search_result:
        lc = lc_file.download()
        lc = lc.remove_outliers(sigma=5)
        lc_binned = lc.bin(bin_time_days)

        color = colors[image_counter % len(colors)] if image_counter <= len(colors) else "#" + ''.join(random.choices('0123456789ABCDEF', k=6))

        plt.figure(figsize=(10, 5))
        lc_binned.plot(marker='o', linewidth=0, color=color, alpha=0.8, markersize=5, label='Binned')

        plt.title(f"TIC {tic_id} - Sector {lc.sector}\n"
                  f"Stellar Temperature: {temperature} K | Binning: {bin_time_minutes} min")
        plt.xlabel("Time [BTJD days]")
        plt.ylabel("Normalized Flux")
        plt.legend()

        output_file = os.path.join(output_folder, f"Sector{image_counter}.png")
        plt.savefig(output_file)
        plt.close()
        print(f"Saved plot: {output_file}")
        image_counter += 1

# List of TIC IDs to process
tic_ids = [
    440801822, 345724317, 329981856, 284300833, 277039287, 269343479, 
    263723967, 238597883, 210904767, 201175570, 169904935, 156115721, 
    124709665, 106997505, 88863718, 65212867, 57299130, 50365310, 21720215
]

# Generate plots for each TIC ID
for tic_id in tic_ids:
    print(f"Processing TIC {tic_id}...")
    plot_sectors_with_temperature(tic_id)