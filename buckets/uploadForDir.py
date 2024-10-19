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

def insert_into_anomalies(supabase: Client, anomaly_id, content, anomaly_set: str):
    if not check_anomaly_exists(supabase, anomaly_id):
        try:
            data = {
                "id": anomaly_id, 
                "content": content, 
                "anomalytype": "zoodexOthers",
                "anomalySet": 'zoodex-nestQuestGo',
            }
            response = supabase.table('anomalies').insert(data).execute()
            print(f"Inserted anomaly with id {anomaly_id} into 'anomalies' table.")
        except Exception as e:
            print(f"Failed to insert anomaly {anomaly_id}: {e}")
    else:
        print(f"Anomaly {anomaly_id} already exists in the database. Skipping insertion.")

def upload_directory_to_supabase(supabase: Client, bucket_name: str, local_directory: str):
    # Iterate over each subfolder in the local directory
    for anomaly_folder in os.listdir(local_directory):
        full_path = os.path.join(local_directory, anomaly_folder)
        if os.path.isdir(full_path):
            # Treat each subfolder as an anomaly
            anomaly_id = anomaly_folder  # Use the folder name as the anomaly ID
            anomaly_set = "telescope-minorPlanet"  # Set a consistent anomaly set
            
            # Insert the anomaly into the database
            insert_into_anomalies(supabase, anomaly_id, anomaly_id, anomaly_set)
            
            # Upload all files from the subfolder
            for root, _, files in os.walk(full_path):
                for file_name in files:
                    if file_name.startswith('.'):
                        continue
                    
                    file_path = os.path.join(root, file_name)
                    relative_path = os.path.relpath(file_path, local_directory)
                    destination_path = f"{anomaly_id}/{Path(relative_path).as_posix()}"

                    upload_file_to_supabase(supabase, bucket_name, file_path, destination_path)

def main():
    supabase = init_supabase_client()
    bucket_name = "zoodex/zoodex-nestQuestGo"
    local_directory = "zoodex/zoodex-nestQuestGo"
    
    upload_directory_to_supabase(supabase, bucket_name, local_directory)

if __name__ == "__main__":
    main()