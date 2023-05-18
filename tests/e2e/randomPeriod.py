import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np
import os

# Define the tic ID of interest
tic_id = "TIC 55525572"

lc = lk.search_lightcurvefile(tic_id).download().SAP_FLUX.remove_nans().normalize()

# Fold the light curve
period = 9.00585
folded_lc = lc.fold(period=period, phase=0.5)

# Bin the light curve
bin_size = 0.001
bins = np.arange(0, 1 + bin_size, bin_size)
binned_lc = folded_lc.bin(bins=bins)

# Convert TimeDelta to seconds
binned_lc.time = binned_lc.time.to_value("second")

# Plot the binned light curve
fig, ax = plt.subplots(figsize=(8, 4))
ax.errorbar(binned_lc.time, binned_lc.flux, binned_lc.flux_err, fmt=".", capsize=0, color="black")
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Flux")
ax.set_title("Phase-folded and binned light curve for TIC " + tic_id)
fig.savefig("output/KOI5737.jpg")