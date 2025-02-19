import os
from supabase import create_client, Client
from pathlib import Path

def init_supabase_client():
    url = "https://hlufptwhzkpkkjztimzo.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsdWZwdHdoemtwa2tqenRpbXpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyOTk3NTUsImV4cCI6MjAzMTg3NTc1NX0.v_NDVWjIU_lJQSPbJ_Y6GkW3axrQWKXfXVsBEAbFv_I"
    return create_client(url, key)

def download_all_files_from_supabase(supabase: Client, bucket_name: str, download_directory: str):
    # List all files in the bucket (including subdirectories)
    files = supabase.storage.from_(bucket_name).list()

    # Iterate over all files and print the exact paths to help debug
    print("Files and folders found in the bucket:")
    for file in files:
        file_path = file['name']
        print(f"Found item: {file_path}")

        # Skip directories (if any exist)
        if file_path.endswith('/'):
            print(f"Skipping directory: {file_path}")
            continue
        
        # Determine the local file path
        local_path = os.path.join(download_directory, file_path)
        
        # Create any directories that don't exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Download the file and handle errors
        try:
            response = supabase.storage.from_(bucket_name).download(file_path)
            with open(local_path, 'wb') as f:
                f.write(response)
            print(f"Downloaded {file_path} -> {local_path}")
        except Exception as e:
            print(f"Failed to download {file_path}: {e}")

def main():
    supabase = init_supabase_client()
    bucket_name = "anomalies"  # Your Supabase bucket name
    download_directory = "backedup_anomalies" 
    
    download_all_files_from_supabase(supabase, bucket_name, download_directory)

if __name__ == "__main__":
    main()