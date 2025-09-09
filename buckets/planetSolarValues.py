import os
import sys
import json
from supabase import create_client
from astroquery.mast import Catalogs

# --- Supabase config (copied from upload.py) ---
def init_supabase_client():
    url = "http://127.0.0.1:54321"
    service_role_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"
    return create_client(url, service_role_key)

def get_tic_anomalies(supabase):
    # Get all anomalies with anomalySet = 'telescope-tess'
    response = supabase.table("anomalies").select("id, content, anomalyConfiguration").eq("anomalySet", "telescope-tess").execute()
    return response.data

def get_tic_properties(tic_id):
    # Query TIC catalog for stellar properties
    target_name = f"TIC {tic_id}"
    try:
        star_info = Catalogs.query_object(target_name, catalog="TIC")
        if len(star_info) == 0:
            return None, None
        temp = star_info[0]['Teff'] if 'Teff' in star_info.columns else None
        radius = star_info[0]['rad'] if 'rad' in star_info.columns else None
        return temp, radius
    except Exception as e:
        print(f"Error querying TIC {tic_id}: {e}")
        return None, None

def update_anomaly_configuration(supabase, anomaly_id, old_config, temp, radius):
    # Parse old_config if it's a string
    if isinstance(old_config, str):
        try:
            config = json.loads(old_config)
        except Exception:
            config = {}
    elif isinstance(old_config, dict):
        config = old_config
    else:
        config = {}
    config['stellar_temperature'] = temp
    config['stellar_radius'] = radius
    try:
        supabase.table("anomalies").update({"anomalyConfiguration": json.dumps(config)}).eq("id", anomaly_id).execute()
        print(f"Updated anomaly {anomaly_id} with temperature={temp}, radius={radius}")
    except Exception as e:
        print(f"Failed to update anomaly {anomaly_id}: {e}")

def main():
    supabase = init_supabase_client()
    anomalies = get_tic_anomalies(supabase)
    print(f"Found {len(anomalies)} anomalies with anomalySet='telescope-tess'")
    for anomaly in anomalies:
        tic_id = anomaly['content']
        anomaly_id = anomaly['id']
        old_config = anomaly.get('anomalyConfiguration')
        if not tic_id:
            print(f"Skipping anomaly {anomaly_id}: no TIC ID in content")
            continue
        temp, radius = get_tic_properties(tic_id)
        if temp is None and radius is None:
            print(f"Could not find properties for TIC {tic_id}")
            continue
        update_anomaly_configuration(supabase, anomaly_id, old_config, temp, radius)

if __name__ == "__main__":
    main()