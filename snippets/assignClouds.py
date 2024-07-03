import os
import random
from supabase import create_client, Client

# Set up Supabase client
supabase_url = 'https://hlufptwhzkpkkjztimzo.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsdWZwdHdoemtwa2tqenRpbXpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyOTk3NTUsImV4cCI6MjAzMTg3NTc1NX0.v_NDVWjIU_lJQSPbJ_Y6GkW3axrQWKXfXVsBEAbFv_I'
supabase: Client = create_client(supabase_url, supabase_key)

# Fetch anomalies with anomalytype 'planet'
anomalies_list = supabase.table("anomalies").select("id").eq("anomalytype", "planet").execute()

# Get the list of image files from the directory
image_directory = "../anomalies/clouds"
image_files = [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))]

# Define a function to upload image to Supabase storage
def upload_to_supabase(filepath, bucket_name, folder_name, file_name):
    with open(filepath, 'rb') as f:
        supabase.storage.from_(bucket_name).upload(f"{folder_name}/{file_name}", f.read(), file_options={"content-type": "image/png"})

# Process each image file
for image_file in image_files:
    # Randomly select an anomaly
    anomaly = random.choice(anomalies_list.data)
    anomaly_id = anomaly['id']

    # Define folder names
    folder_name = f"{anomaly_id}/clouds"

    # Define full file path
    file_path = os.path.join(image_directory, image_file)

    # Upload the image file to Supabase storage
    upload_to_supabase(file_path, 'anomalies', folder_name, image_file)

    print(f"Uploaded {image_file} to folder {folder_name} in Supabase storage.")