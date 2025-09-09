# TIC 158793333 / KOI-4871 Spectroscopy Data README

## Overview
This directory contains exported data and analysis from a high-resolution optical spectrum of TIC 158793333 (also known as KOI-4871, 2MASS J19140696+4216345, Gaia DR2 2102326709749646848, and other aliases). The FITS file was obtained with the CTIO 1.5m telescope and the CHIRON spectrograph, and covers the star associated with the Kepler Object of Interest KOI-4871, a candidate exoplanet system.

## What is in the FITS file?
- **Raw Data:** The FITS file contains a 3D array: (orders, pixels, types). Each 'order' is a segment of the echelle spectrum, covering a specific wavelength range. Each 'type' may represent different data products (e.g., flux, error).
- **Header:** The FITS header includes metadata about the observation, instrument, and detector settings, but does not contain direct wavelength calibration (no CRVAL1/CDELT1 per order).

## What does the spectrum show?
- **Star, not planet:** The spectrum is of the host star, not the planet candidate. Direct spectroscopy of planets is extremely rare; most planet composition studies use transit or secondary eclipse techniques, which are not applicable here.
- **Stellar Composition:** The spectrum contains absorption lines from elements in the star's atmosphere (e.g., hydrogen, sodium, calcium, magnesium, iron). These lines allow astronomers to determine the star's chemical composition, temperature, gravity, and radial velocity.
- **No direct planet info:** The spectrum does not directly reveal the composition of the planet(s) KOI-4871.01 or KOI-4871.02. However, stellar parameters are crucial for interpreting transit data and inferring planet properties.

## Exported Data
- **CSV files:** Each order and type is exported as a CSV file for further analysis.
- **Summary statistics:** `summary_stats.csv` contains mean, standard deviation, min, max, and signal-to-noise ratio (SNR) for each order/type.
- **Combined plots:** For each type, a PNG image overlays all orders, showing the normalized spectrum. If wavelength calibration is available, known spectral lines (H-alpha, Na D, Ca II, etc.) are marked.
- **Header info:** `fits_header.txt` contains all FITS header metadata for reference.

## How to use this data
- **Stellar analysis:** Use the combined plots and CSVs to identify absorption lines and measure their properties. This can reveal the star's metallicity, temperature, and other physical parameters.
- **Planet context:** The star's properties are essential for understanding the planet candidates (KOI-4871.01, KOI-4871.02) detected by Kepler. Precise stellar parameters improve estimates of planet size, orbit, and habitability.
- **Further work:** For detailed abundance analysis, wavelength calibration per order is needed (consult instrument docs or calibration files). Advanced analysis may require fitting synthetic spectra or using tools like iSpec, MOOG, or SME.

## References
- [ExoFOP-Kepler page for KOI-4871](https://exofop.ipac.caltech.edu/kepler/target.php?id=4871)
- [CHIRON spectrograph documentation](https://www.ctio.noirlab.edu/CHIRON/)
- [Astropy FITS documentation](https://docs.astropy.org/en/stable/io/fits/)

## Contact
For questions about this data or analysis, contact the observer listed in the FITS header or your project PI.
