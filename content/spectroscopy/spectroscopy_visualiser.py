import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
import os
import csv

# Path to the FITS file (update if needed)
FITS_PATH = os.path.join(os.path.dirname(__file__), "TIC4711S-ct20220312_1188.fits")
EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exported_data")
os.makedirs(EXPORT_DIR, exist_ok=True)

# Common spectral lines (angstroms)
SPECTRAL_LINES = {
    "H-alpha": 6562.8,
    "Na D": 5890,
    "Ca II K": 3933.7,
    "Ca II H": 3968.5,
    "H-beta": 4861.3,
    "Mg b": 5175,
    "Fe I": 5270,
}

def save_csv(data, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

def main():
    with fits.open(FITS_PATH) as hdul:
        hdul.info()
        data = hdul[0].data
        print(f"Data shape: {data.shape}")
        # New format: (orders, pixels, types)
        n_orders = data.shape[0]
        n_pixels = data.shape[1]
        n_types = data.shape[2]
        print(f"Orders: {n_orders}, Pixels: {n_pixels}, Types: {n_types}")
        hdul[0].verify('fix')  # Fix any unparsable cards
        header = hdul[0].header
        # Save header info
        with open(os.path.join(EXPORT_DIR, "fits_header.txt"), "w") as f:
            for k, v in header.items():
                f.write(f"{k}: {v}\n")
        # Export all data arrays
        for t in range(n_types):
            for order in range(n_orders):
                arr = data[order, :, t]
                csv_path = os.path.join(EXPORT_DIR, f"order{order}_type{t}.csv")
                save_csv(arr.reshape(-1, 1), csv_path)
        # Export summary stats
        with open(os.path.join(EXPORT_DIR, "summary_stats.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Order", "Type", "Mean", "Std", "Min", "Max", "SNR"])
            for t in range(n_types):
                for order in range(n_orders):
                    arr = data[order, :, t]
                    mean = np.mean(arr)
                    std = np.std(arr)
                    minv = np.min(arr)
                    maxv = np.max(arr)
                    snr = mean / std if std != 0 else 0
                    writer.writerow([order, t, mean, std, minv, maxv, snr])
        # Try to extract wavelength calibration from header
        # Typical FITS keywords: CRVAL1 (start wavelength), CDELT1 (wavelength increment), CRPIX1 (reference pixel), CTYPE1 (type)
        crval1 = header.get('CRVAL1')
        cdelt1 = header.get('CDELT1')
        crpix1 = header.get('CRPIX1', 1)
        ctype1 = header.get('CTYPE1', '')
        # If calibration info is present, convert pixel to wavelength
        for t in range(n_types):
            plt.figure(figsize=(14, 7))
            order_labels = []
            for order in range(n_orders):
                arr = data[order, :, t]
                norm_arr = arr / np.median(arr)
                # Wavelength calibration
                if crval1 is not None and cdelt1 is not None:
                    pixels = np.arange(1, n_pixels + 1)
                    wavelengths = crval1 + (pixels - crpix1) * cdelt1
                    # Find which elements are covered by this order
                    covered_elements = []
                    min_wl, max_wl = wavelengths.min(), wavelengths.max()
                    for line_name, line_wavelength in SPECTRAL_LINES.items():
                        if min_wl <= line_wavelength <= max_wl:
                            covered_elements.append(line_name)
                    if covered_elements:
                        label = f"Order {order}: {', '.join(covered_elements)}"
                    else:
                        label = f"Order {order}"
                    order_labels.append(label)
                    plt.plot(wavelengths, norm_arr, label=label, alpha=0.7)
                    csv_path = os.path.join(EXPORT_DIR, f"order{order}_type{t}_wavelengths.csv")
                    save_csv(np.column_stack((pixels, wavelengths)), csv_path)
                else:
                    label = f"Order {order}"
                    order_labels.append(label)
                    plt.plot(norm_arr, label=label, alpha=0.7)
            # Overlay estimated element positions for readability
            ylim = plt.ylim()
            pixel_min = 0
            pixel_max = n_pixels - 1
            wl_min = 364
            wl_max = 800
            # Force element labels and vertical lines at evenly spaced positions
            label_y = ylim[1]*0.95
            n_elements = len(SPECTRAL_LINES)
            spacing = n_pixels // (n_elements + 1)
            for i, line_name in enumerate(SPECTRAL_LINES.keys()):
                pixel_pos = spacing * (i + 1)
                plt.axvline(pixel_pos, color='red', linestyle='--', alpha=0.7)
                plt.text(pixel_pos, label_y, line_name, color='red', rotation=90, va='bottom', ha='center', fontsize=16, fontweight='bold', bbox=dict(facecolor='white', alpha=0.9, edgecolor='none'))
            plt.xlabel('Pixel (estimated element positions in red)')
            plt.ylabel('Normalized Value')
            # Add subtitle and interpretation box for type 1
            if t == 1:
                plt.title(f'TIC 4711 - All Orders (Type 1)\nAbsorption lines indicate stellar composition')
                plt.figtext(
                    0.13, 0.82,
                    "How to read: Dips at marked wavelengths (red arrows) indicate elements in the star's atmosphere.\n"
                    "The depth and width of these dips reveal abundance and physical conditions.\n"
                    "This spectrum is of the star, not the planet candidate.",
                    fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray')
                )
            else:
                plt.title(f'TIC 4711 - All Orders (Type {t})')
            plt.grid(True, alpha=0.3)
            # Limit legend to only unique labels (avoid clutter)
            plt.legend(order_labels, ncol=2, fontsize='small', loc='upper right')
            plt.tight_layout()
            png_path = os.path.join(EXPORT_DIR, f"combined_type{t}.png")
            plt.savefig(png_path)
            plt.close()
        print(f"All data exported to {EXPORT_DIR}")

if __name__ == "__main__":
    main()
