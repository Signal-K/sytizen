import os
from supabase import create_client, Client
from pathlib import Path

# Initialize Supabase client
def init_supabase_client():
    url = "http://127.0.0.1:54321"  
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
    return create_client(url, key)

# Function to upload a file to Supabase storage
def upload_file_to_supabase(supabase: Client, bucket_name: str, file_path: str, destination_path: str):
    try:
        # Check if file already exists
        existing_file = supabase.storage.from_(bucket_name).get(destination_path)
        if existing_file.status_code == 200:  # File exists
            # Delete the existing file
            supabase.storage.from_(bucket_name).remove([destination_path])
            print(f"Deleted existing file: {destination_path}")
        
        # Upload the new file
        with open(file_path, "rb") as file:
            response = supabase.storage.from_(bucket_name).upload(destination_path, file)
            print(f"Uploaded {file_path} -> {destination_path}")
            return True
    except Exception as e:
        print(f"Failed to upload {file_path} -> {destination_path}: {e}")
        return False

# Function to upload all files in a directory to Supabase
def upload_directory_to_supabase(supabase: Client, bucket_name: str, local_directory: str):
    for root, dirs, files in os.walk(local_directory):
        for file_name in files:
            if file_name.startswith('.'):
                continue

            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, local_directory)
            destination_path = Path(relative_path).as_posix()

            # Upload file to Supabase storage
            upload_file_to_supabase(supabase, bucket_name, file_path, destination_path)

def main():
    supabase = init_supabase_client()
    bucket_name = "anomalies"  
    local_directory = "anomalies" 
    
    upload_directory_to_supabase(supabase, bucket_name, local_directory)

if __name__ == "__main__":
    main()