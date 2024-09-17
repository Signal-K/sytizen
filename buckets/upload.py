import os
from supabase import create_client, Client
from pathlib import Path

# Initialize Supabase client
def init_supabase_client():
    url = "http://127.0.0.1:54321"  # Replace with your Supabase URL
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"  # Replace with your key
    return create_client(url, key)

# Upload file to Supabase bucket
def upload_file_to_supabase(supabase: Client, bucket_name: str, file_path: str, destination_path: str):
    with open(file_path, "rb") as file:
        try:
            response = supabase.storage.from_(bucket_name).upload(destination_path, file)
            print(f"Uploaded {file_path} -> {destination_path}")
        except Exception as e:
            print(f"Failed to upload {file_path} -> {destination_path}: {e}")

# Recursive function to upload all files in directory
def upload_directory_to_supabase(supabase: Client, bucket_name: str, local_directory: str):
    for root, dirs, files in os.walk(local_directory):
        for file_name in files:
            if file_name.startswith('.'):
                # Skip hidden files (e.g., .DS_Store)
                continue
            
            file_path = os.path.join(root, file_name)
            
            # Create relative path for Supabase storage to mirror local structure
            relative_path = os.path.relpath(file_path, local_directory)
            destination_path = Path(relative_path).as_posix()  # Ensure path uses forward slashes
            
            # Upload file
            upload_file_to_supabase(supabase, bucket_name, file_path, destination_path)

# Main function
def main():
    supabase = init_supabase_client()
    bucket_name = "clouds"  # Use your Supabase bucket name
    local_directory = "clouds"  # Folder you want to upload (in this case, anomalies)
    
    upload_directory_to_supabase(supabase, bucket_name, local_directory)

if __name__ == "__main__":
    main()