from flask import Flask, request, jsonify
import httpx
import os

app = Flask(__name__)

# Read Supabase URL and API Key from environment variables
SUPABASE_URL = os.environ.get('NEXT_PUBLIC_SUPABASE_URL')
SUPABASE_API_KEY = os.environ.get('NEXT_PUBLIC_SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_API_KEY:
    raise ValueError("Supabase URL and API Key are required. Make sure to set them in your environment variables.")

@app.route('/get_planet', methods=['POST'])
def get_planet():
    request_data = request.get_json()

    planet_id = request_data.get('planetId')

    if not planet_id:
        return jsonify({"error": "Planet ID is required"}), 400

    # Construct the Supabase URL with query parameters directly in the URL
    supabase_url = f"{SUPABASE_URL}/rest/v1/planetsss?id=eq.{planet_id}&select=*"
    
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
            return jsonify(data[0])
        else:
            return jsonify({"error": "Planet not found"}), 404
    else:
        return jsonify({"error": "Error fetching data from Supabase"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)