from flask import Flask, request, jsonify, render_template
import httpx
import os
import lightkurve as lk
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Read Supabase URL and API Key from environment variables
SUPABASE_URL = os.environ.get('NEXT_PUBLIC_SUPABASE_URL')
SUPABASE_API_KEY = os.environ.get('NEXT_PUBLIC_SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_API_KEY:
    raise ValueError("Supabase URL and API Key are required. Make sure to set them in your environment variables.")

@app.route('/get_planet', methods=['POST', 'GET'])
def get_planet():
    if request.method == 'POST':
        request_data = request.get_json()

        planet_id = request_data.get('planetId')

        if not planet_id:
            return jsonify({"error": "Planet ID is required"}), 400

        # Construct the Supabase URL with query parameters directly in the URL
        supabase_url = f"{SUPABASE_URL}/rest/v1/planetsss?id=eq.{planet_id}&select=ticId"  # Updated to select ticId field only

        # Set up headers with Supabase API key
        headers = {
            'apikey': SUPABASE_API_KEY,
            'Content-Type': 'application/json',
        }

        # Send a GET request to Supabase
        with httpx.Client() as client:
            response = client.get(supabase_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data:
                tic_id = data[0].get('ticId')  # Corrected to 'ticId'
                return jsonify({"planet_id": planet_id, "ticId": tic_id})  # Corrected to 'ticId'
            else:
                return jsonify({"error": "Planet not found"}), 404
        else:
            return jsonify({"error": "Error fetching data from Supabase"}), response.status_code

    return render_template('planet_input.html')

@app.route('/plot_lightcurve/<planet_id>')
def plot_lightcurve(planet_id):
    tic_id = "KOI-4871"

    # Download the light curve
    lc = lk.search_lightcurvefile(tic_id, quarter=1).download()

    # Create the plot
    fig, ax = plt.subplots()
    lc.plot(ax=ax)

    # Save the plot to a BytesIO object
    plot_buffer = BytesIO()
    plt.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)

    # Encode the plot as base64 to pass to the frontend
    plot_base64 = base64.b64encode(plot_buffer.read()).decode('utf-8')

    return render_template('lightcurve.html', plot_base64=plot_base64)

if __name__ == '__main__':
    app.run(debug=True)