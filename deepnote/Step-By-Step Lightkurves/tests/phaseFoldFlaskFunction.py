import lightkurve as lk
import matplotlib.pyplot as plt

# Define the target and download the light curve data
target = "KOI-1144.01"  # The KOI ID for KOI 11446443
search_result = lk.search_lightcurvefile(target)
lc_file = search_result.download().PDCSAP_FLUX.remove_nans()

# Correct systematics using a Savitzky-Golay filter
lc_clean = lc_file.flatten(window_length=101).remove_outliers(sigma=5)

# Phase fold the light curve using the period from the KOI table
period = 2.48419  # The period from the KOI table
phase_folded = lc_clean.fold(period=period, t0=lc_clean.time[np.argmax(lc_clean.flux)])

# Binning the phase-folded light curve
bin_size = 0.002  # Adjust the bin size based on your preference
binned = phase_folded.bin(binsize=bin_size)

# Plotting the phase-folded and binned light curve
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(phase_folded.time, phase_folded.flux, 'ko', markersize=3)
plt.xlabel("Phase")
plt.ylabel("Flux")
plt.title("Phase Folded Light Curve")

plt.subplot(2, 1, 2)
plt.plot(binned.time, binned.flux, 'ko', markersize=5)
plt.xlabel("Phase")
plt.ylabel("Flux")
plt.title(f"Phase Folded and Binned Light Curve (bin size={bin_size})")

plt.tight_layout()
plt.show()