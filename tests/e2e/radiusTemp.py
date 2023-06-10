import lightkurve as lk
import matplotlib.pyplot as plt
import os

# Define the target TIC ID
target = "KOI-5737"

# Download and process the light curve
lc = lk.search_lightcurvefile(target).download().PDCSAP_FLUX.remove_nans().normalize()

# Fold the light curve on the transit period
period = 9.029
epoch_time = 2454953.52025
folded_lc = lc.fold(period, epoch_time=epoch_time)

# Plot and save the phase-folded light curve
fig, ax = plt.subplots()
folded_lc.plot(ax=ax)
ax.set_xlabel('Phase')
ax.set_ylabel('Normalized Flux')
if not os.path.exists('output'):
    os.makedirs('output')
plt.savefig('output/5737.jpg')


"""import lightkurve as lk
from astropy import units as u
import time

# time = time * u.day
# flux = flux * u.electron/u.second

def generate_lightcurve_koi456():
    # Download data using the target name
    target = "KOI-456"
    lc = lk.search_lightcurvefile(target).download().PDCSAP_FLUX.remove_nans().normalize()
    
    # Remove outliers
    lc = lc.remove_outliers(sigma=6)#, ignore_nan=True)
    
    # Fold lightcurve using period and epoch
    period = 6.02991
    epoch = 132.25422
    folded_lc = lc.fold(period=period, epoch_time=epoch)
    
    # Plot the folded lightcurve
    fig = folded_lc.plot()
    fig.savefig("output/KOI-456.jpg")
    
    # Estimate planet properties
    r_planet = folded_lc.estimate_radius()
    t_planet = folded_lc.estimate_temperature()
    p_orbit = period
    
    # Save planet properties to supabase
    # ...
    
    print("Finished generating lightcurve for KOI-456.")


generate_lightcurve_koi456()"""