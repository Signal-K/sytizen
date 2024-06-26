from flask import Flask, jsonify, request
from supabase import create_client, Client
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import requests
import os

app = Flask(__name__)

# Supabase credentials
SUPABASE_URL = 'https://hlufptwhzkpkkjztimzo.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsdWZwdHdoemtwa2tqenRpbXpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyOTk3NTUsImV4cCI6MjAzMTg3NTc1NX0.v_NDVWjIU_lJQSPbJ_Y6GkW3axrQWKXfXVsBEAbFv_I'
SUPABASE_STORAGE_URL = 'https://hlufptwhzkpkkjztimzo.supabase.co/storage/v1'

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route('/')
def index():
    try:
        # Fetch anomalies of type "planet"
        response = supabase.from_("anomalies").select("*").eq("anomalytype", "planet").execute()
        if response['status'] == 200:
            anomalies = response['data']
            for anomaly in anomalies:
                anomaly_id = anomaly['id']
                tic_id = anomaly['configuration']['ticId']
                create_lightkurve_graph(anomaly_id, tic_id)
            return 'Lightkurve graphs created and uploaded successfully.'
        else:
            return 'Failed to fetch anomalies from Supabase.'
    except Exception as e:
        return f'Error: {str(e)}'

@app.route('/upload-lightcurve', methods=['POST'])
def upload_lightcurve():
    try:
        data = request.get_json()
        tic_id = data.get('ticId')
        anomaly_id = data.get('anomalyId')

        if not tic_id or not anomaly_id:
            return jsonify({'message': 'TIC Id and anomaly Id are required'}), 400

        # Generate lightcurve graph and upload to Supabase
        success = generate_and_upload_lightcurve(tic_id, anomaly_id)
        
        if success:
            return jsonify({'message': f'Lightcurve uploaded successfully for Anomaly ID: {anomaly_id}'}), 200
        else:
            return jsonify({'message': 'Failed to generate or upload lightcurve image'}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 500

def generate_and_upload_lightcurve(tic_id, anomaly_id):
    try:
        # Generate lightcurve graph
        img_bytes = generate_lightcurve_graph(tic_id)
        if img_bytes:
            # Upload image to Supabase storage
            upload_image_to_supabase(tic_id, anomaly_id, img_bytes)
            return True
        else:
            return False
    except Exception as e:
        print(f'Error: {str(e)}')
        return False

def generate_lightcurve_graph(tic_id):
    try:
        # Retrieve lightcurve data using lightkurve
        lc = lk.search_lightcurvefile(tic_id).download().PDCSAP_FLUX
        # Fold the lightcurve
        folded_lc = lc.fold(period=lc.period)
        
        # Plot the folded lightcurve
        plt.figure(figsize=(10, 6))
        folded_lc.scatter(color='lightblue', alpha=0.6)
        plt.title(f'Folded Lightcurve for TIC ID: {tic_id}')
        plt.xlabel('Phase')
        plt.ylabel('Flux')
        plt.grid(True)
        
        # Save plot to BytesIO object
        img_bytes = BytesIO()
        plt.savefig(img_bytes, format='png')
        img_bytes.seek(0)
        plt.close()
        
        return img_bytes
    except Exception as e:
        print(f'Error generating lightcurve graph: {str(e)}')
        return None

def upload_image_to_supabase(tic_id, anomaly_id, img_bytes):
    try:
        # Upload image to Supabase storage under "anomalies" folder with anomaly_id
        upload_url = f'{SUPABASE_STORAGE_URL}/object/public/anomalies/{anomaly_id}/{tic_id}_phase.png'
        headers = {
            'apikey': SUPABASE_KEY,
            'Content-Type': 'image/png'
        }
        response = requests.post(upload_url, headers=headers, data=img_bytes)
        if response.status_code == 201:
            print(f'Image uploaded successfully for TIC ID: {tic_id} under Anomaly ID: {anomaly_id}')
            return True
        else:
            print(f'Failed to upload image for TIC ID: {tic_id} under Anomaly ID: {anomaly_id}')
            return False
    except Exception as e:
        print(f'Error uploading image to Supabase: {str(e)}')
        return False


def create_lightkurve_graph(anomaly_id, tic_id):
    try:
        # Example URL for lightkurve data (replace with your data retrieval method)
        lightkurve_url = f"https://example.com/lightkurve/{tic_id}"
        response = requests.get(lightkurve_url)
        if response.status_code == 200:
            data = pd.read_csv(BytesIO(response.content))
            # Example phase-folded plot (replace with your actual plot generation logic)
            plt.figure(figsize=(8, 6))
            plt.scatter(data['phase'], data['flux'], color='lightblue', alpha=0.6)
            plt.xlabel('Phase')
            plt.ylabel('Flux')
            plt.title(f'Phase-folded lightkurve for TIC ID: {tic_id}')
            plt.grid(True)
            # Save plot to a BytesIO object
            img_bytes = BytesIO()
            plt.savefig(img_bytes, format='png')
            img_bytes.seek(0)
            # Upload image to Supabase storage
            upload_image_to_supabase(anomaly_id, img_bytes)
            plt.close()
        else:
            print(f'Failed to fetch lightkurve data for TIC ID: {tic_id}')
    except Exception as e:
        print(f'Error creating lightkurve graph: {str(e)}')


def upload_image_to_supabase(anomaly_id, img_bytes):
    try:
        # Upload image to Supabase storage under "anomalies" folder with anomaly_id
        upload_url = f'{SUPABASE_STORAGE_URL}/object/public/anomalies/{anomaly_id}/phase.png'
        headers = {
            'apikey': SUPABASE_KEY,
            'Content-Type': 'image/png'
        }
        response = requests.post(upload_url, headers=headers, data=img_bytes)
        if response.status_code == 201:
            print(f'Image uploaded successfully for anomaly ID: {anomaly_id}')
        else:
            print(f'Failed to upload image for anomaly ID: {anomaly_id}')
    except Exception as e:
        print(f'Error uploading image to Supabase: {str(e)}')


if __name__ == '__main__':
    app.run(debug=True)
