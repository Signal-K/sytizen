import lightkurve as lk
"""import numpy as np
import pandas as pd
import astropy.units as u
import astropy.io.fits as pf
from glob import glob as glob"""

# from ..app import app

@app.route('/planets/classify', methods=['POST'])
def classify_planet_sector_data():
    data = request.get_json()
    ticId = data['ticId']

    transit_depth = 1 - 0.9989 # this is from the above phase folded figure
    R_star = 2.04354 * u.Rsun # this is the radius of the parent star for the specific target. Get value from ExoFOP

    def planet_radius (transit_depth, R_star):
        r_pl_solar_radius = np.sqrt(transit_depth) * R_star
        r_pl_Earth = r_pl_solar_radius.to(u.Rearth).value
        print("Radius of the planet: {} Earth radii".format(round(r_pl_Earth, 2)))

    planet_radius(transit_depth, R_star)
    return planet_radius

@app.route('/planets/classify', methods=['GET'])
def classify_planet_sector_data_radius():
    transit_depth = 1 - 0.9989 # this is from the above phase folded figure
    R_star = 2.04354 * u.Rsun # this is the radius of the parent star for the specific target. Get value from ExoFOP

    def planet_radius (transit_depth, R_star):
        r_pl_solar_radius = np.sqrt(transit_depth) * R_star
        r_pl_Earth = r_pl_solar_radius.to(u.Rearth).value
        print("Radius of the planet: {} Earth radii".format(round(r_pl_Earth, 2)))

    planet_radius(transit_depth, R_star)
    return planet_radius