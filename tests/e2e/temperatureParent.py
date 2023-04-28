import lightkurve as lk

# Search for a light curve of the object
search_result = lk.search_lightcurvefile('KIC 8462852', mission='Kepler')
lc = search_result.download().PDCSAP_FLUX.remove_nans().remove_outliers()

# Estimate the temperature of the parent star
temperature = lc.estimate_temperature()
print(f"The estimated temperature of the parent star is {temperature:.0f} K")
