import os
import requests
from supabase import create_client, Client
import logging

# Initialize Supabase client
supabase_url = 'https://hlufptwhzkpkkjztimzo.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsdWZwdHdoemtwa2tqenRpbXpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyOTk3NTUsImV4cCI6MjAzMTg3NTc1NX0.v_NDVWjIU_lJQSPbJ_Y6GkW3axrQWKXfXVsBEAbFv_I'
supabase: Client = create_client(supabase_url, supabase_key)

# Define the initial folder path
initial_folder = '../anomalies/planets'

# Ensure the initial folder exists
if not os.path.exists(initial_folder):
    os.makedirs(initial_folder)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base URL for public access to the storage bucket
public_base_url = f'{supabase_url}/storage/v1/object/public/anomalies/'

# Function to download images from Supabase storage and save them to the local file system
def download_images_from_supabase():
    offset = 0
    while True:
        try:
            # List objects in the 'anomalies' bucket with pagination
            files = supabase.storage.from_('anomalies').list('', {'limit': 1000, 'offset': offset})
            if not files:
                logger.info("No more files to download.")
                break
        except Exception as e:
            logger.error(f"Error listing files from Supabase: {e}")
            break

        for file in files:
            file_path = file['name']
            anomaly_id = file_path.split('/')[0]  # Extract the anomaly ID from the file path
            file_name = file_path.split('/')[-1]  # Extract the file name

            # Create a directory for the anomaly ID if it doesn't exist
            anomaly_folder = os.path.join(initial_folder, anomaly_id)
            if not os.path.exists(anomaly_folder):
                os.makedirs(anomaly_folder)

            # Construct the public URL for the file
            public_file_url = f'{public_base_url}{file_path}'
            local_file_path = os.path.join(anomaly_folder, file_name)

            try:
                # Download the file from Supabase storage
                response = requests.get(public_file_url)
                response.raise_for_status()  # Check for HTTP errors

                # Save the file to the local directory
                with open(local_file_path, 'wb') as f:
                    f.write(response.content)

                logger.info(f"Downloaded {file_name} to {local_file_path}")

            except requests.RequestException as e:
                logger.error(f"Error downloading {file_path}: {e}")

        offset += 1000

# Run the download function
if __name__ == "__main__":
    download_images_from_supabase()
