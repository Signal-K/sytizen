import numpy as np
from lightkurve import search_targetpixelfile

tpf = search_targetpixelfile('EPIC 246067459').download()
aperture_mask = np.zeros(tpf.shape[1:], dtype=bool)
aperture_mask[15:20, 15:20] = True
lc = tpf.to_lightcurve(aperture_mask=aperture_mask).remove_nans().remove_outliers()
pg = lc.to_periodogram(method='bls', period=np.arange(0.2, 2, 0.001), duration=0.1)
pg.plot()
period = pg.period_at_max_power
transit_time = lc.fold(period).time[np.argmin(lc.fold(period).flux)]
rp_rs = np.sqrt(lc.depth[float(np.argmin(lc.fold(period).flux))])
r_star = 1.0 # assuming the star is the same size as the Sun
r_planet = rp_rs * r_star * 109.2
print('Planet radius = {:.2f} Earth radii'.format(r_planet))
