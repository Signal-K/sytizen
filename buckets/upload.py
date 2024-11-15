import os
from supabase import create_client, Client
from pathlib import Path

# Initialize Supabase client
def init_supabase_client():
    url = "http://127.0.0.1:54321"  
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
    return create_client(url, key)

def upload_file_to_supabase(supabase: Client, bucket_name: str, file_path: str, destination_path: str):
    with open(file_path, "rb") as file:
        try:
            response = supabase.storage.from_(bucket_name).upload(destination_path, file)
            print(f"Uploaded {file_path} -> {destination_path}")
            return True
        except Exception as e:
            if "Duplicate" in str(e):
                print(f"File already exists: {file_path}. Proceeding with database insertion.")
                return True  
            print(f"Failed to upload {file_path} -> {destination_path}: {e}")
            return False

def check_anomaly_exists(supabase: Client, anomaly_id):
    try:
        response = supabase.table('anomalies').select("*").eq("id", anomaly_id).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error checking for anomaly {anomaly_id}: {e}")
        return False

def check_anomaly_needs_avatar_update(supabase: Client, anomaly_id):
    try:
        # Check if the anomaly exists and if avatar_url is missing
        response = supabase.table('anomalies').select("avatar_url").eq("id", anomaly_id).execute()
        if len(response.data) > 0:
            return response.data[0]["avatar_url"] is None
        return False
    except Exception as e:
        print(f"Error checking avatar_url for anomaly {anomaly_id}: {e}")
        return False

def insert_or_update_anomalies(supabase: Client, anomaly_id, content, anomaly_set: str, avatar_url: str):
    if not check_anomaly_exists(supabase, anomaly_id):
        try:
            # Insert new anomaly with avatar_url
            data = {
                "id": anomaly_id, 
                "content": content, 
                "anomalytype": "telescopeClouds",
                "anomalySet": anomaly_set,
                "parentAnomaly": 69,
                "avatar_url": avatar_url
            }
            response = supabase.table('anomalies').insert(data).execute()
            print(f"Inserted anomaly with id {anomaly_id} into 'anomalies' table.")
        except Exception as e:
            print(f"Failed to insert anomaly {anomaly_id}: {e}")
    else:
        # Check if the anomaly needs its avatar_url updated
        if check_anomaly_needs_avatar_update(supabase, anomaly_id):
            try:
                response = supabase.table('anomalies').update({"avatar_url": avatar_url}).eq("id", anomaly_id).execute()
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
    supabase = init_supabase_client()
    bucket_name = "telescope/automaton-aiForMars"
    local_directory = "automatons/automatons-ai4Mars" 
    
    upload_directory_to_supabase(supabase, bucket_name, local_directory)

if __name__ == "__main__":
    main()