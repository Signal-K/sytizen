import os
import sys
import json
from supabase import create_client
from astroquery.mast import Catalogs
from astroquery.simbad import Simbad
from astroquery.gaia import Gaia
import numpy as np

# --- Supabase config (copied from upload.py) ---
def init_supabase_client():
    url = "http://127.0.0.1:54321"
    service_role_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"
    return create_client(url, service_role_key)

def get_tic_anomalies(supabase):
    # Get all anomalies with anomalySet = 'telescope-tess'
    response = supabase.table("anomalies").select("id, content, anomalyConfiguration").eq("anomalySet", "telescope-tess").execute()
    return response.data


def is_valid_number(val):
    try:
        if val is None:
            return False
        if isinstance(val, str) and (val.lower() == 'nan' or val.strip() == ''):
            return False
        if isinstance(val, float) and np.isnan(val):
            return False
        v = float(val)
        return np.isfinite(v)
    except Exception:
        return False

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

def get_simbad_properties(tic_id):
    # Query SIMBAD for stellar properties
    try:
        result = Simbad.query_object(f"TIC {tic_id}")
        if result is None:
            return None, None
        temp = result['Teff'][0] if 'Teff' in result.colnames else None
        radius = result['Radius'][0] if 'Radius' in result.colnames else None
        return temp, radius
    except Exception as e:
        print(f"Error querying SIMBAD for TIC {tic_id}: {e}")
        return None, None

def get_gaia_properties(tic_id):
    # Query Gaia for stellar properties using TIC crossmatch
    try:
        # Gaia doesn't use TIC IDs directly, but some crossmatch tables exist
        # Here, we try to search by source_id if available, else skip
        # This is a placeholder for a real crossmatch implementation
        # You may want to implement a real crossmatch using Vizier or other services
        return None, None
    except Exception as e:
        print(f"Error querying Gaia for TIC {tic_id}: {e}")
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
        # Fallback to SIMBAD if needed
        if not (is_valid_number(temp) and is_valid_number(radius)):
            simbad_temp, simbad_radius = get_simbad_properties(tic_id)
            if is_valid_number(simbad_temp):
                temp = simbad_temp
            if is_valid_number(simbad_radius):
                radius = simbad_radius
        # Fallback to Gaia if still missing
        if not (is_valid_number(temp) and is_valid_number(radius)):
            gaia_temp, gaia_radius = get_gaia_properties(tic_id)
            if is_valid_number(gaia_temp):
                temp = gaia_temp
            if is_valid_number(gaia_radius):
                radius = gaia_radius

        # Fallback: try KOI and KIC prefixes if still missing
        if not (is_valid_number(temp) and is_valid_number(radius)):
            koi_id = f"KOI {tic_id}"
            kic_id = f"KIC {tic_id}"
            # Try KOI
            koi_temp, koi_radius = get_tic_properties(koi_id)
            if is_valid_number(koi_temp):
                temp = koi_temp
            if is_valid_number(koi_radius):
                radius = koi_radius
            # Try SIMBAD KOI
            if not (is_valid_number(temp) and is_valid_number(radius)):
                simbad_koi_temp, simbad_koi_radius = get_simbad_properties(koi_id)
                if is_valid_number(simbad_koi_temp):
                    temp = simbad_koi_temp
                if is_valid_number(simbad_koi_radius):
                    radius = simbad_koi_radius
            # Try KIC
            if not (is_valid_number(temp) and is_valid_number(radius)):
                kic_temp, kic_radius = get_tic_properties(kic_id)
                if is_valid_number(kic_temp):
                    temp = kic_temp
                if is_valid_number(kic_radius):
                    radius = kic_radius
            # Try SIMBAD KIC
            if not (is_valid_number(temp) and is_valid_number(radius)):
                simbad_kic_temp, simbad_kic_radius = get_simbad_properties(kic_id)
                if is_valid_number(simbad_kic_temp):
                    temp = simbad_kic_temp
                if is_valid_number(simbad_kic_radius):
                    radius = simbad_kic_radius

        # Only update if we have both values
        if not (is_valid_number(temp) and is_valid_number(radius)):
            print(f"Could not find valid properties for TIC {tic_id} (anomaly {anomaly_id}) after all fallbacks including KOI/KIC.")
            continue
        update_anomaly_configuration(supabase, anomaly_id, old_config, temp, radius)

if __name__ == "__main__":
    main()