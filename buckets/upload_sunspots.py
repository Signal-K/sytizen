import os
import sys
import signal
from supabase import create_client, Client
from pathlib import Path
from typing import List, Tuple
from dotenv import load_dotenv

def signal_handler(sig, frame):
    print('\n\nUpload interrupted by user. Exiting gracefully...')
    sys.exit(0)

# Load environment variables
load_dotenv()

# Supabase configurations
CLOUD_CONFIG = {
    "url": os.getenv("SUPABASE_CLOUD_URL", "https://hlufptwhzkpkkjztimzo.supabase.co"),
    "service_role_key": os.getenv("SUPABASE_CLOUD_SERVICE_ROLE_KEY"),
    "anon_key": os.getenv("SUPABASE_CLOUD_ANON_KEY")
}

LOCAL_CONFIG = {
    "url": os.getenv("SUPABASE_LOCAL_URL", "http://127.0.0.1:54321"),
    "service_role_key": os.getenv("SUPABASE_LOCAL_SERVICE_ROLE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"),
    "anon_key": os.getenv("SUPABASE_LOCAL_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0")
}

def init_supabase_clients() -> Tuple[Client, Client]:
    """Initialize both local and cloud Supabase clients"""
    try:
        cloud_client = create_client(CLOUD_CONFIG["url"], CLOUD_CONFIG["service_role_key"])
        print("✓ Connected to cloud Supabase")
    except Exception as e:
        print(f"Warning: Could not connect to cloud Supabase: {e}")
        cloud_client = None
    
    try:
        local_client = create_client(LOCAL_CONFIG["url"], LOCAL_CONFIG["service_role_key"])
        print("✓ Connected to local Supabase")
    except Exception as e:
        print(f"Warning: Could not connect to local Supabase: {e}")
        local_client = None
    
    if not cloud_client and not local_client:
        raise Exception("Failed to connect to both Supabase instances")
    
    return cloud_client, local_client

def upload_file_to_supabase(supabase: Client, bucket_name: str, file_path: str, destination_path: str, instance_name: str) -> bool:
    """Upload a file to Supabase storage"""
    with open(file_path, "rb") as file:
        try:
            response = supabase.storage.from_(bucket_name).upload(
                destination_path, 
                file, 
                file_options={"upsert": "true"}
            )
            print(f"  [{instance_name}] Uploaded {file_path} -> {destination_path}")
            return True
        except Exception as e:
            if "Duplicate" in str(e):
                print(f"  [{instance_name}] File already exists: {file_path}. Trying to update...")
                try:
                    file.seek(0)  # Reset file pointer
                    response = supabase.storage.from_(bucket_name).update(destination_path, file)
                    print(f"  [{instance_name}] Updated {file_path} -> {destination_path}")
                    return True
                except Exception as update_error:
                    print(f"  [{instance_name}] Failed to update {file_path}: {update_error}")
                    return False
            else:
                print(f"  [{instance_name}] Failed to upload {file_path}: {e}")
                return False

def check_anomaly_exists(supabase: Client, anomaly_id: int, instance_name: str) -> bool:
    """Check if an anomaly already exists in the database"""
    try:
        response = supabase.table("anomalies").select("*").eq("id", anomaly_id).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"  [{instance_name}] Error checking for anomaly {anomaly_id}: {e}")
        return False

def insert_or_update_anomaly(supabase: Client, anomaly_data: dict, instance_name: str) -> bool:
    """Insert or update an anomaly in the database"""
    anomaly_id = anomaly_data["id"]
    
    if not check_anomaly_exists(supabase, anomaly_id, instance_name):
        try:
            response = supabase.table("anomalies").insert(anomaly_data).execute()
            print(f"  [{instance_name}] Inserted anomaly {anomaly_id} into anomalies table")
            return True
        except Exception as e:
            print(f"  [{instance_name}] Failed to insert anomaly {anomaly_id}: {e}")
            return False
    else:
        try:
            # Update avatar_url if it's different
            response = supabase.table("anomalies").update({
                "avatar_url": anomaly_data["avatar_url"],
                "content": anomaly_data["content"]
            }).eq("id", anomaly_id).execute()
            print(f"  [{instance_name}] Updated anomaly {anomaly_id}")
            return True
        except Exception as e:
            print(f"  [{instance_name}] Failed to update anomaly {anomaly_id}: {e}")
            return False

def process_sunspot_files(cloud_client: Client, local_client: Client, bucket_name: str, local_directory: str):
    """Process and upload sunspot files to both Supabase instances"""
    
    if not os.path.exists(local_directory):
        print(f"Error: Directory {local_directory} does not exist")
        return
    
    files_processed = 0
    files_failed = 0
    
    for root, dirs, files in os.walk(local_directory):
        for file_name in files:
            # Skip hidden files and non-image files
            if file_name.startswith('.'):
                continue
            
            if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                print(f"Skipping non-image file: {file_name}")
                continue
            
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, local_directory)
            destination_path = Path(relative_path).as_posix()
            
            # Extract anomaly ID from filename (without extension)
            file_name_without_ext = os.path.splitext(file_name)[0]
            try:
                anomaly_id = int(file_name_without_ext)
            except ValueError:
                print(f"Warning: Could not extract numeric ID from filename: {file_name}")
                continue
            
            print(f"\nProcessing: {file_name} (ID: {anomaly_id})")
            
            # Prepare anomaly data (structured for sunspots)
            anomaly_data = {
                "id": anomaly_id,
                "content": str(anomaly_id),
                "ticId": None,
                "anomalytype": "telescopeOthers",
                "type": None,
                "radius": None,
                "mass": None,
                "density": None,
                "gravity": None,
                "temperatureEq": None,
                "temperature": None,
                "smaxis": None,
                "orbital_period": None,
                "classification_status": None,
                "avatar_url": f"{bucket_name}/{destination_path}",
                "deepnote": None,
                "lightkurve": None,
                "configuration": None,
                "parentAnomaly": None,
                "anomalySet": "sunspot",
                "anomalyConfiguration": None
            }
            
            cloud_upload_success = False
            local_upload_success = False
            
            # Upload to cloud Supabase
            if cloud_client:
                cloud_upload_success = upload_file_to_supabase(
                    cloud_client, bucket_name, file_path, destination_path, "CLOUD"
                )
                if cloud_upload_success:
                    insert_or_update_anomaly(cloud_client, anomaly_data, "CLOUD")
            
            # Upload to local Supabase
            if local_client:
                local_upload_success = upload_file_to_supabase(
                    local_client, bucket_name, file_path, destination_path, "LOCAL"
                )
                if local_upload_success:
                    insert_or_update_anomaly(local_client, anomaly_data, "LOCAL")
            
            if cloud_upload_success or local_upload_success:
                files_processed += 1
            else:
                files_failed += 1
    
    print("\n" + "="*60)
    print(f"Upload Summary:")
    print(f"  Files processed: {files_processed}")
    print(f"  Files failed: {files_failed}")
    print("="*60)

def main():
    # Register signal handler for graceful exit on Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("="*60)
    print("  Sunspot Anomaly Upload Script")
    print("  Uploads to both LOCAL and CLOUD Supabase instances")
    print("="*60)
    print()
    
    # Initialize clients
    try:
        cloud_client, local_client = init_supabase_clients()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Configuration: allow CLI override or auto-detect sunspots folder
    cli_dir = None
    if len(sys.argv) > 1:
        cli_dir = sys.argv[1]

    known_dirs = [
        "telescope/telescope-sunspots",
        "citizen/buckets/telescope/telescope-sunspots",
    ]

    if cli_dir:
        local_directory = cli_dir
    else:
        # pick the first existing known dir
        local_directory = None
        for d in known_dirs:
            if os.path.exists(d):
                local_directory = d
                break
        if not local_directory:
            # fallback to the first known path (user will be warned)
            local_directory = known_dirs[0]

    # derive bucket name from local_directory if it looks like 'telescope/...'
    bucket_name = local_directory.replace('\\', '/').lstrip('./')
    
    print(f"\nConfiguration:")
    print(f"  Bucket: {bucket_name}")
    print(f"  Local Directory: {local_directory}")
    print(f"  Anomaly Set: sunspot")
    print(f"  Anomaly Type: telescopeOthers")
    print()
    
    # Check if bucket exists
    if cloud_client:
        try:
            buckets = cloud_client.storage.list_buckets()
            bucket_names = [bucket.name for bucket in buckets]
            print(f"Cloud buckets available: {bucket_names}")
        except Exception as e:
            print(f"Warning: Could not list cloud buckets: {e}")
    
    if local_client:
        try:
            buckets = local_client.storage.list_buckets()
            bucket_names = [bucket.name for bucket in buckets]
            print(f"Local buckets available: {bucket_names}")
        except Exception as e:
            print(f"Warning: Could not list local buckets: {e}")
    
    print()
    
    try:
        process_sunspot_files(cloud_client, local_client, bucket_name, local_directory)
        print("\n✓ Upload completed successfully!")
    except KeyboardInterrupt:
        print('\n\nUpload interrupted by user. Exiting gracefully...')
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Upload failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
