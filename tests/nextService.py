from flask import Flask, request, jsonify
import lightkurve as lk
from astroquery.mast import Catalogs
import numpy as np
from flask_cors import CORS
from math import log10

app = Flask(__name__)
CORS(app)

app.config['TIMEOUT'] = 600

data_store = [] # Empty list -> will cross-reference db data at next stage

@app.route('/receive_data', methods=['POST'])
def receive_data():
    request_data = request.get_json()

    planet_name = request_data.get('planetName')
    user_name = request_data.get('userName')
    planet_data = request_data.get('planetData')

    if not planet_name or not user_name or not planet_data:
        return jsonify({"error": "Invalid data format"}), 400

    # Save the received data to the data store
    data_store.append({
        "planetName": planet_name,
        "userName": user_name,
        "planetData": planet_data
    })

    return jsonify({"message": "Data received successfully", "data_store": data_store}), 200

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(data_store)

@app.route('/process_tic_id', methods=['POST'])
def process_tic_id():
    request_data = request.get_json()

    tic_id = request_data.get('ticId')

    if not tic_id:
        return jsonify({"error": "TIC ID is required"}), 400

    try:
        # Use lightkurve to process the TIC ID and generate a period value
        search_result = lk.search_lightcurvefile(tic_id)#, quarter=1)
        if not search_result:
            return jsonify({"error": "No light curve data found for the given TIC ID"}), 404

        # Download the light curve data
        lc = search_result.download()

        # Calculate the period (dummy example: using the first observed period in days)
        period = lc.to_periodogram().period_at_max_power

        # Append the processed data to the data store
        data_store.append({
            "ticId": tic_id,
            "period": period
        })

        return jsonify({"message": "TIC ID processed successfully", "period": period, "data_store": data_store}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/flux_variability', methods=['POST'])
def flux_variability():
    request_data = request.get_json()

    tic_id = request_data.get('ticId')

    if not tic_id:
        return jsonify({"error": "TIC ID is required"}), 400

    try:
        # Use lightkurve to process the TIC ID and calculate the flux variability metric (e.g., standard deviation)
        search_result = lk.search_lightcurvefile(tic_id)
        
        if len(search_result) == 0:
            return jsonify({"error": "No light curve data found for the given TIC ID"}), 404

        # Download the first available light curve
        lc = search_result[0].download().SAP_FLUX  # Access the 'SAP_FLUX' attribute directly

        # Access the scalar value of the flux data and calculate the standard deviation
        flux_data = lc.flux.value

        # Check if the flux data is empty or contains NaN values
        if len(flux_data) == 0 or np.isnan(flux_data).all():
            return jsonify({"ticId": tic_id, "flux_stddev": None, "error": "Unable to calculate flux variability due to data characteristics"}), 200

        # Calculate the standard deviation and convert to a Python float
        flux_stddev = float(np.std(flux_data))

        return jsonify({"ticId": tic_id, "flux_stddev": flux_stddev}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_star_info', methods=['POST'])
def get_star_info():
    try:
        tic_id = request.json.get("ticId")
        result = Catalogs.query_criteria(catalog="Tic", ID=tic_id)

        if len(result) == 0:
            return jsonify({"error": "No information found for the given TIC ID."})

        star = result[0]
        Tmag = star['Tmag']  # Tmag as a substitute for color index
        BV = (Tmag - 2.85) / (-0.075)  # Calculate B-V color index
        color = BV

        mass = star['mass']  # Stellar mass in solar masses
        radius = star['rad']  # Stellar radius in solar radii
        luminosity = star['lum']  # Stellar luminosity in solar luminosities

        # Use assumptions to estimate metallicity based on color, star type, mass, radius, and luminosity
        metallicity = 0.0  # Initialize metallicity

        # Adjust metallicity based on mass, radius, and luminosity (for illustrative purposes)
        if mass > 2.0 and radius > 2.0 and luminosity > 10.0:
            metallicity -= 0.5  # Lower metallicity for high-mass giants

        return jsonify({
            "Color (B-V Index Approximation)": color,
            "Stellar Mass (solar masses)": mass,
            "Stellar Radius (solar radii)": radius,
            "Stellar Luminosity (solar luminosities)": luminosity,
        #    "Star Type": star_type,
        #    "Star": star,
            "Estimated Metallicity ([Fe/H])": metallicity
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/get_metallicity', methods=['POST'])
def get_metallicity():
    try:
        data = request.get_json()
        tic_id = data['tic_id']

        # Query the MAST catalog for the star's information
        result = Catalogs.query_criteria(catalog="Tic", ID=tic_id)
        
        if len(result) == 0:
            return jsonify({"error": "No information found for the given TIC ID."}), 404

        # Extract the metallicity information (assuming it's labeled as [Fe/H])
        metallicity = result[0]['[Fe/H]']

        return jsonify({"metallicity": metallicity})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)