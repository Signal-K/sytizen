import os
import sys
import signal
from supabase import create_client, Client
from pathlib import Path
from dotenv import load_dotenv

def signal_handler(sig, frame):
    print('\n\nUpload interrupted by user. Exiting gracefully...')
    sys.exit(0)

# Initialize Supabase client
def init_supabase_client():
    # Load environment variables from .env.local in the parent directory
    env_path = os.path.join(os.path.dirname(__file__), '../../.env.local')
    load_dotenv(env_path)
    
    url = os.getenv('NEXT_PUBLIC_SUPABASE_URL', 'http://127.0.0.1:54321')
    service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    anon_key = os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY')
    
    print(f"Using Supabase URL: {url}")
    
    # Try service role key first, fallback to anon key
    try:
        if service_role_key:
            return create_client(url, service_role_key)
        else:
            print("Warning: No service role key found, using anonymous key")
            return create_client(url, anon_key)
    except Exception as e:
        print(f"Warning: Failed to create client with service role key: {e}")
        print("Trying with anonymous key...")
        return create_client(url, anon_key)

def upload_file_to_supabase(supabase: Client, bucket_name: str, file_path: str, destination_path: str):
    with open(file_path, "rb") as file:
        try:
            # Determine content type based on file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            content_type = "image/jpeg"  # Default for bumble images
            if file_ext in ['.jpg', '.jpeg']:
                content_type = "image/jpeg"
            elif file_ext == '.png':
                content_type = "image/png"
            elif file_ext == '.gif':
                content_type = "image/gif"
            elif file_ext == '.webp':
                content_type = "image/webp"
            
            # Try uploading with upsert=True and correct content type
            response = supabase.storage.from_(bucket_name).upload(
                destination_path, 
                file, 
                file_options={"content-type": content_type, "upsert": "true"}
            )
            print(f"Uploaded {file_path} -> {destination_path}")
            return True
        except Exception as e:
            if "Duplicate" in str(e):
                print(f"File already exists: {file_path}. Trying to update...")
                try:
                    # Try updating the existing file
                    response = supabase.storage.from_(bucket_name).update(destination_path, file)
                    print(f"Updated {file_path} -> {destination_path}")
                    return True
                except Exception as update_error:
                    print(f"Failed to update {file_path}: {update_error}")
                    return False
            elif "Unauthorized" in str(e) or "signature verification failed" in str(e):
                print(f"Authorization failed for {file_path}. Check your API key permissions.")
                print("You may need to:")
                print("1. Use a service role key instead of anonymous key")
                print("2. Update your RLS policies to allow uploads")
                print("3. Make the bucket public for uploads")
                return False
            else:
                print(f"Failed to upload {file_path} -> {destination_path}: {e}")
                return False

def check_anomaly_exists(supabase: Client, anomaly_id):
    try:
        response = supabase.table("anomalies").select("*").eq("id", anomaly_id).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error checking for anomaly {anomaly_id}: {e}")
        return False

def check_anomaly_needs_avatar_update(supabase: Client, anomaly_id):
    try:
        response = supabase.table("anomalies").select("avatar_url").eq("id", anomaly_id).execute()
        if len(response.data) > 0:
            return response.data[0]["avatar_url"] is None
        return False
    except Exception as e:
        print(f"Error checking avatar_url for anomaly {anomaly_id}: {e}")
        return False

def insert_or_update_anomalies(supabase: Client, anomaly_id, content, avatar_url: str):
    if not check_anomaly_exists(supabase, anomaly_id):
        try:
            # Insert a new anomaly for bumble
            data = {
                "id": anomaly_id,
                "content": content,
                "anomalytype": "bumble",
                "anomalySet": "bumble",
                "avatar_url": avatar_url
            }
            response = supabase.table("anomalies").insert(data).execute()
            print(f"Inserted anomaly with id {anomaly_id} into 'anomalies' table with anomalySet 'bumble'.")
        except Exception as e:
            print(f"Failed to insert anomaly {anomaly_id}: {e}")
    else:
        if check_anomaly_needs_avatar_update(supabase, anomaly_id):
            try:
                response = supabase.table("anomalies").update({"avatar_url": avatar_url}).eq("id", anomaly_id).execute()
                print(f"Updated anomaly {anomaly_id} with new avatar_url.")
            except Exception as e:
                print(f"Failed to update avatar_url for anomaly {anomaly_id}: {e}")
        else:
            print(f"Anomaly {anomaly_id} already has an avatar_url. Skipping update.")

def upload_directory_to_supabase(supabase: Client, bucket_name: str, local_directory: str):
    for root, dirs, files in os.walk(local_directory):
        for file_name in files:
            if file_name.startswith('.'):
                continue

            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, local_directory)
            destination_path = Path(relative_path).as_posix()

            # Use the filename (without extension) as anomaly_id
            file_name_without_ext = os.path.splitext(file_name)[0]
            anomaly_id = file_name_without_ext
            content = f"Bumble {file_name_without_ext}"

            # Upload file and if successful, insert or update the anomaly
            if upload_file_to_supabase(supabase, bucket_name, file_path, destination_path):
                # Create the avatar_url with the relative path in the Supabase bucket
                avatar_url = f"{bucket_name}/{destination_path}"
                insert_or_update_anomalies(supabase, anomaly_id, content, avatar_url)

def main():
    # Register signal handler for graceful exit on Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=== Supabase Storage Upload Script - Bumble ===")
    print("Starting upload process for bumble files...")
    print()
    
    supabase = init_supabase_client()
    bucket_name = "bumble"
    local_directory = "bumble"
    
    # Check if bucket exists and is accessible
    try:
        buckets = supabase.storage.list_buckets()
        bucket_names = [bucket.name for bucket in buckets]
        if bucket_name not in bucket_names:
            print(f"Warning: Bucket '{bucket_name}' not found. Available buckets: {bucket_names}")
        else:
            print(f"Found bucket '{bucket_name}'. Starting upload...")
    except Exception as e:
        print(f"Error checking buckets: {e}")
    
    try:
        upload_directory_to_supabase(supabase, bucket_name, local_directory)
        print("\nUpload completed successfully!")
    except KeyboardInterrupt:
        print('\n\nUpload interrupted by user. Exiting gracefully...')
        sys.exit(0)
    except Exception as e:
        print(f"\nUpload failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
