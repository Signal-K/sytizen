import os
from supabase import create_client, Client

def init_supabase_client():
    url = "http://127.0.0.1:54321"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
    return create_client(url, key)

def fetch_files_from_bucket(supabase: Client, bucket_name: str):
    storage = supabase.storage.from_(bucket_name)
    response = storage.list()
    return response  # This returns a list of files directly

def download_file_from_bucket(supabase: Client, bucket_name: str, file_name: str, download_path: str):
    storage = supabase.storage.from_(bucket_name)
    print(f"Attempting to download: {bucket_name}/{file_name}")
    try:
        file_data = storage.download(file_name)
        with open(download_path, 'wb') as file:
            file.write(file_data)
        print(f"Downloaded {file_name} to {download_path}")
    except Exception as e:
        print(f"Error downloading {file_name}: {e}")

def create_directory_for_bucket(bucket_name: str):
    directory_path = os.path.join(os.getcwd(), bucket_name)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return directory_path

def download_files_from_buckets(supabase: Client, bucket_names: list):
    for bucket_name in bucket_names:
        print(f"Processing bucket: {bucket_name}")
        files = fetch_files_from_bucket(supabase, bucket_name)
        bucket_directory = create_directory_for_bucket(bucket_name)
        for file in files:
            file_name = file['name']
            download_path = os.path.join(bucket_directory, file_name)
            try:
                print(f"Downloading file: {file_name} to {download_path}")
                download_file_from_bucket(supabase, bucket_name, file_name, download_path)
            except Exception as e:
                print(f"Error downloading {file_name}: {e}")
        print(f"Finished downloading files from bucket: {bucket_name}\n")

def main():
    supabase = init_supabase_client()
    bucket_names = ['anomalies', 'zoodex', 'media', 'avatars', 'clouds', 'telescope']
    download_files_from_buckets(supabase, bucket_names)

if __name__ == "__main__":
    main()