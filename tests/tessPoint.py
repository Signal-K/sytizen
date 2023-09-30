from flask import Flask, request, jsonify
import requests
from astroquery.mast import Catalogs

app = Flask(__name__)

TIC_API_URL = "https://exo.mast.stsci.edu/api/v0.1/exoplanets/keplerid/"

@app.route("/get_star_info", methods=["GET"])
def get_star_info():
    tic_id = request.args.get("tic_id")

    try:
        # Make an HTTP request to the TIC API to retrieve star information
        response = requests.get(f"{TIC_API_URL}{tic_id}")
        response_data = response.json()

        # Extract relevant information from the response, e.g., star name
        star_name = response_data.get("star_name")

        return jsonify({"star_name": star_name})
    except Exception as e:
        return jsonify({"error": str(e)})


def get_stellar_parameters(tic_id):
    try:
        # Query the MAST catalog for stellar parameters
        result = Catalogs.query_criteria(catalog="Tic", ID=tic_id)

        if result is not None:
            # Extract relevant stellar parameters from the result
            star_name = result['TICID'][0]
            radius = result['rad'][0]  # Stellar radius
            metallicity = result['met'][0]  # Metallicity
            mass = result['mass'][0]  # Stellar mass
            density = result['rho'][0]  # Stellar density
            luminosity = result['lum'][0]  # Luminosity

            # Return the extracted data
            stellar_data = {
                "star_name": star_name,
                "radius": radius,
                "metallicity": metallicity,
                "mass": mass,
                "density": density,
                "luminosity": luminosity
            }
            return stellar_data
        else:
            return {"error": "Star not found in the MAST catalog"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(debug=True)