import os
import sys
import signal
from supabase import create_client, Client
from pathlib import Path

def signal_handler(sig, frame):
    print('\n\nUpload interrupted by user. Exiting gracefully...')
    sys.exit(0)

# Initialize Supabase client
def init_supabase_client():
    url = "http://127.0.0.1:54321" #'https://api.starsailors.space' # "http://127.0.0.1:54321"  
    # You need a service role key for storage uploads, not the anon key
    # Get this from your Supabase dashboard under Settings > API
    service_role_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU" #"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsdWZwdHdoemtwa2tqenRpbXpvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxNjI5OTc1NSwiZXhwIjoyMDMxODc1NzU1fQ.JYo6Phyuc_a6TsctnvUUBvf8OVXQHDipiwI4l_5an3Q"  # Replace with actual service role key
    anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0" #"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsdWZwdHdoemtwa2tqenRpbXpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyOTk3NTUsImV4cCI6MjAzMTg3NTc1NX0.v_NDVWjIU_lJQSPbJ_Y6GkW3axrQWKXfXVsBEAbFv_I"
    
    # Try service role key first, fallback to anon key
    try:
        return create_client(url, service_role_key)
    except:
        print("Warning: Using anonymous key - storage uploads may fail")
        return create_client(url, anon_key)
def upload_file_to_supabase(supabase: Client, bucket_name: str, file_path: str, destination_path: str):
    with open(file_path, "rb") as file:
        try:
            # Try uploading with upsert=True to handle existing files
            response = supabase.storage.from_(bucket_name).upload(
                destination_path, 
                file, 
                file_options={"upsert": "true"}
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

def insert_or_update_anomalies(supabase: Client, anomaly_id, content, anomaly_set: str, avatar_url: str):
    if not check_anomaly_exists(supabase, anomaly_id):
        try:
            data = {
                "id": anomaly_id, 
                "content": content, 
                "anomalytype": "planet", # "telescopeSignal", # "telescopeMinor", # "telescopeMinor", # "satellitePics", # "gaseousMapping", # "planet",
                "anomalySet": "telescope-tess", # "telescope-awa", # 'active-asteroids', # "telescope-minorPlanet", # "satellite-planetFour", # "lidar-jovianVortexHunter", # "cloudspottingOnMars", # "telescope-tess", # anomaly_set,
                # "parentAnomaly": 50,
                "avatar_url": avatar_url
            }
            response = supabase.table("anomalies").insert(data).execute()
            print(f"Inserted anomaly with id {anomaly_id} into 'anomalies' table.")
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

            anomaly_set = Path(root).name 

            anomaly_id = Path(file_name).stem
            try:
                anomaly_id = int(anomaly_id) 
                content = anomaly_id 
            except ValueError:
                anomaly_id = anomaly_set 
                content = anomaly_set  

            # Upload file and if successful, insert or update the anomaly
            if upload_file_to_supabase(supabase, bucket_name, file_path, destination_path):
                # Create the avatar_url with the relative path in the Supabase bucket
                avatar_url = f"{bucket_name}/{destination_path}"
                insert_or_update_anomalies(supabase, anomaly_id, content, anomaly_set, avatar_url)

def main():
    # Register signal handler for graceful exit on Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=== Supabase Storage Upload Script ===")
    print("Starting upload process...")
    print()
    
    supabase = init_supabase_client()
    bucket_name = "anomalies" # 'telescope/telescope-areWeAlone' # 'telescope/automatons-ai4Mars' # "telescope/telescope-dailyMinorPlanet" # "telescope/satellite-planetFour" # "telescope/lidar-jovianVortexHunter" # "clouds" #telescope/telescope-dailyMinorPlanet"
    local_directory = "anomalies" # 'telescope/telescope-areWeAlone' # "automatons/automatons-ai4Mars" # "telescope/telescope-dailyMinorPlanet" # "satellite/satellite-planetFour" # "satellite/lidar-jovianVortexHunters" # "clouds" #"telescope/telescope-dailyMinorPlanet" 
    
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