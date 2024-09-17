import os
import random
import time
from supabase import create_client, Client

# Set up Supabase client
supabase_url = 'https://hlufptwhzkpkkjztimzo.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsdWZwdHdoemtwa2tqenRpbXpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyOTk3NTUsImV4cCI6MjAzMTg3NTc1NX0.v_NDVWjIU_lJQSPbJ_Y6GkW3axrQWKXfXVsBEAbFv_I'
supabase: Client = create_client(supabase_url, supabase_key)

# Get the list of image files from the directory
image_directory = "../anomalies/clouds"
image_files = [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))]

# Define a function to upload image to Supabase storage
def upload_to_supabase(filepath, bucket_name, folder_name, file_name, retries=3):
    for attempt in range(retries):
        try:
            # Check if the file already exists in the bucket
            existing_files = supabase.storage.from_(bucket_name).list(folder_name)
            existing_file_names = [file['name'] for file in existing_files]
            if file_name in existing_file_names:
                print(f"File {file_name} already exists in {folder_name}. Trying a different folder.")
                raise FileExistsError("File already exists")  # Trigger an exception to try a different folder
            
            # Upload the file
            with open(filepath, 'rb') as f:
                supabase.storage.from_(bucket_name).upload(f"{folder_name}/{file_name}", f.read(), file_options={"content-type": "image/png"})
            print(f"Uploaded {file_name} to folder {folder_name} in Supabase storage.")
            break  # Exit loop if upload is successful
        
        except FileExistsError:
            # Generate a new folder name to avoid conflicts
            new_anomaly_id = random.choice(anomaly_ids)
            new_folder_name = f"{new_anomaly_id}/clouds"
            print(f"Retrying with a new folder {new_folder_name} for file {file_name}.")
            folder_name = new_folder_name  # Update folder name for retry
            
        except Exception as e:
            print(f"Error during upload: {e}. Retrying ({attempt + 1}/{retries})...")
            if attempt == retries - 1:
                print(f"Failed to upload {file_name} after {retries} attempts.")
            else:
                time.sleep(2)  # Wait before retrying

# Fetch anomalies with anomalytype 'planet'
anomalies_list = supabase.table("anomalies").select("id").eq("anomalytype", "planet").execute()
anomaly_ids = [anomaly['id'] for anomaly in anomalies_list.data]

# Get existing folders from the `anomalies` bucket
def list_folders(bucket_name):
    """List all folders in the given bucket."""
    folders = []
    response = supabase.storage.from_(bucket_name).list("")  # List all items in the bucket
    items = response
    for item in items:
        path_parts = item['name'].split('/')
        if len(path_parts) > 1 and path_parts[1] == 'clouds':
            continue  # Skip paths already under a clouds folder
        if len(path_parts) == 1 and path_parts[0].isdigit():  # Check if it's a folder with an ID
            folders.append(path_parts[0])
    return folders

# Identify folders that do not have a `clouds` directory
def identify_folders_without_clouds(bucket_name):
    """Identify folders without a `clouds` directory."""
    folders = list_folders(bucket_name)
    folders_without_clouds = []
    for folder in folders:
        clouds_dir_exists = any(clouds_dir['name'] == f"{folder}/clouds" for clouds_dir in supabase.storage.from_(bucket_name).list(folder))
        if not clouds_dir_exists:
            folders_without_clouds.append(folder)
    return folders_without_clouds

folders_without_clouds = identify_folders_without_clouds('anomalies')

# Define a function to upload images to folders that do not have a `clouds` directory
def upload_to_folders_without_clouds(image_files, folders):
    """Upload images to folders that do not have a `clouds` directory."""
    for image_file in image_files:
        for folder in folders:
            file_path = os.path.join(image_directory, image_file)
            folder_name = f"{folder}/clouds"
            upload_to_supabase(file_path, 'anomalies', folder_name, image_file)
            break  # Ensure that we only upload to one folder per image

# Upload images to folders that do not have a `clouds` directory
upload_to_folders_without_clouds(image_files, folders_without_clouds)

# Upload remaining images to existing `clouds` directories or new folders
def upload_to_existing_or_new_folders(image_files):
    """Upload images to existing or new folders."""
    for image_file in image_files:
        file_path = os.path.join(image_directory, image_file)
        for _ in range(5):  # Retry up to 5 times to find a folder
            # Randomly select an anomaly
            anomaly_id = random.choice(anomaly_ids)

            # Define folder names
            folder_name = f"{anomaly_id}/clouds"

            # Try to upload the image file to Supabase storage
            try:
                upload_to_supabase(file_path, 'anomalies', folder_name, image_file)
                break  # Exit loop if upload is successful
            except Exception as e:
                print(f"Error during upload to {folder_name}: {e}")
                time.sleep(2)  # Wait before retrying
        else:
            print(f"Failed to upload {image_file} after several attempts.")

# Upload remaining images to existing or new folders
upload_to_existing_or_new_folders(image_files)