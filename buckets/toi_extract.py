import os
import sys
import json
import signal
import random
import numpy as np
import pandas as pd
import lightkurve as lk
import matplotlib.pyplot as plt
from supabase import create_client, Client
from astroquery.mast import Catalogs
from pathlib import Path

# --- Signal Handler for graceful exit ---
def signal_handler(sig, frame):
    print('\n\nProcess interrupted by user. Exiting gracefully...')
    sys.exit(0)

# --- Supabase Configuration ---
def init_supabase_client():
    """Initializes and returns a Supabase client."""
    url = "http://127.0.0.1:54321"
    service_role_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"
    try:
        return create_client(url, service_role_key)
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
        sys.exit(1)

# --- Data Validation ---
def is_valid_number(val):
    """Checks if a value is a valid, finite number."""
    if val is None:
        return False
    if isinstance(val, str) and (val.lower() == 'nan' or val.strip() == ''):
        return False
    try:
        return np.isfinite(float(val))
    except (ValueError, TypeError):
        return False

# --- Light Curve Plotting ---
def plot_light_curve(lc, star_id, sector_info, output_folder, stellar_props):
    """Generates and saves a light curve plot for a given sector."""
    bin_time_minutes = 30
    bin_time_days = bin_time_minutes / (24 * 60)
    
    try:
        lc_clean = lc.remove_outliers(sigma=5)
        lc_binned = lc_clean.bin(time_bin_size=bin_time_days)

        plt.figure(figsize=(12, 6))
        fig = plt.gcf()
        ax = plt.gca()
        fig.patch.set_facecolor('white')
        ax.patch.set_facecolor('#f0f0f0')

        lc_binned.plot(ax=ax, marker='o', markersize=4, linewidth=0, color='royalblue', alpha=0.8, label=f'Binned ({bin_time_minutes} min)')
        
        temp = stellar_props.get('Teff', 'N/A')
        radius = stellar_props.get('rad', 'N/A')
        
        plt.title(f"Light Curve for {star_id} - Sector {sector_info}", fontsize=14, pad=20)
        plt.xlabel("Time [BTJD]", fontsize=12)
        plt.ylabel("Normalized Flux", fontsize=12)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        
        output_file = os.path.join(output_folder, f"sector_{sector_info}.png")
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"  - Saved plot: {output_file}")
        return output_file
    except Exception as e:
        print(f"  - Error plotting sector {sector_info}: {e}")
        return None

# --- Supabase Operations ---
def upload_file_to_supabase(supabase: Client, bucket_name: str, file_path: str, destination_path: str):
    """Uploads a file to a specified Supabase storage bucket."""
    try:
        with open(file_path, "rb") as file:
            supabase.storage.from_(bucket_name).upload(
                destination_path, file, file_options={"upsert": "true"}
            )
        print(f"  - Uploaded {file_path} to {destination_path}")
        return True
    except Exception as e:
        print(f"  - Failed to upload {file_path}: {e}")
        return False

def insert_or_update_anomaly(supabase: Client, anomaly_data: dict):
    """Inserts or updates an anomaly record in the Supabase table."""
    anomaly_id = anomaly_data['id']
    try:
        # Use upsert to either insert a new record or update an existing one
        supabase.table("anomalies").upsert(anomaly_data).execute()
        print(f"  - Successfully upserted anomaly {anomaly_id} into Supabase.")
    except Exception as e:
        print(f"  - Failed to upsert anomaly {anomaly_id}: {e}")

# --- Main Processing Logic ---
def process_tic(supabase: Client, tic_id_num: int):
    """Main function to process a single TIC ID."""
    tic_id_str = f"TIC {tic_id_num}"
    
    print(f"\n{'='*60}\nProcessing {tic_id_str}\n{'='*60}")

    # 1. Query for stellar parameters
    try:
        star_info_table = Catalogs.query_object(tic_id_str, catalog="TIC")
        if len(star_info_table) == 0:
            print(f"No data found for {tic_id_str} in TIC catalog. Skipping.")
            return
        toi_info = star_info_table[0]
    except Exception as e:
        print(f"Failed to query stellar parameters for {tic_id_str}: {e}")
        return

    # 2. Prepare local directory for generated files
    base_folder = "anomalies"
    output_folder = os.path.join(base_folder, str(tic_id_num))
    os.makedirs(output_folder, exist_ok=True)

    # 3. Collect stellar properties
    stellar_props = {
        'Teff': toi_info.get('Teff'),
        'rad': toi_info.get('rad'),
        'mass': toi_info.get('mass'),
        'logg': toi_info.get('logg'),
        'MH': toi_info.get('MH'), # Stellar metallicity
        'sectors': toi_info.get('sector')
    }
    
    stellar_props_cleaned = {k: v for k, v in stellar_props.items() if is_valid_number(v) or (isinstance(v, str) and v)}
    
    print("Stellar Properties:")
    for key, val in stellar_props_cleaned.items():
        print(f"  - {key}: {val}")

    # 4. Search and process light curves for all available sectors
    print("\nSearching for light curves...")
    try:
        search_result = lk.search_lightcurve(tic_id_str, author="SPOC")
        if len(search_result) == 0:
            print("No SPOC light curves found. Trying TESS-SPOC.")
            search_result = lk.search_lightcurve(tic_id_str, author="TESS-SPOC")
        
        if len(search_result) == 0:
            print(f"No light curves found for {tic_id_str}. Skipping.")
            return
            
        print(f"Found {len(search_result)} light curve(s).")
    except Exception as e:
        print(f"Error searching for light curves for {tic_id_str}: {e}")
        return

    # 5. Download, plot, and upload light curves
    uploaded_files = []
    for lc_item in search_result:
        try:
            lc = lc_item.download()
            if lc:
                plot_path = plot_light_curve(lc, tic_id_str, lc.sector, output_folder, stellar_props_cleaned)
                if plot_path:
                    destination_path = Path(os.path.relpath(plot_path, base_folder)).as_posix()
                    if upload_file_to_supabase(supabase, "anomalies", plot_path, destination_path):
                        uploaded_files.append(destination_path)
        except Exception as e:
            print(f"  - Failed to process sector {lc_item.mission[-1]}: {e}")

    # 6. Prepare and upload anomaly data to Supabase
    if not uploaded_files:
        print("No files were successfully uploaded. Skipping Supabase anomaly creation.")
        return
        
    anomaly_id = int(tic_id_num)
    avatar_url = f"anomalies/{uploaded_files[0]}"
    
    stellar_props_cleaned['light_curve_images'] = uploaded_files
    
    anomaly_data = {
        "id": anomaly_id,
        "content": tic_id_str,
        "anomalytype": "planet",
        "anomalySet": "telescope-tess",
        "avatar_url": avatar_url,
        "anomalyConfiguration": json.dumps(stellar_props_cleaned, allow_nan=False)
    }
    
    print("\nPreparing to update Supabase...")
    insert_or_update_anomaly(supabase, anomaly_data)
    print(f"Finished processing {tic_id_str}.")


def main():
    """Main execution function."""
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=== TIC Data Extraction and Upload Script ===")
    
    supabase = init_supabase_client()
    
    # Specific list of TIC IDs to process
    tic_ids_to_process = [
        110795273, 55871761, 442530946, 126325985, 11270200,
        77202722, 71841620, 431016234, 188500604, 76835246, 68952448
    ]
    
    # Process each TIC ID
    for tic_id in tic_ids_to_process:
        process_tic(supabase, tic_id)

    print(f"\n{'='*60}\nAll processing complete!\n{'='*60}")

if __name__ == "__main__":
    main()
