import lightkurve as lk

search_result = lk.search_lightcurve('KIC 8462852', mission='Kepler')
lc = search_result.download().PDCSAP_FLUX.remove_nans().remove_outliers()

teff = search_result.target_table['teff'][0]
print(f"The temperature of the parent star is {teff} K")