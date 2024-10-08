import os
import shutil
import lightkurve as lk
import matplotlib.pyplot as plt
from supabase import create_client, Client
import re  # Import the regex library

# Initialize Supabase client
supabase_url = 'https://hlufptwhzkpkkjztimzo.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsdWZwdHdoemtwa2tqenRpbXpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyOTk3NTUsImV4cCI6MjAzMTg3NTc1NX0.v_NDVWjIU_lJQSPbJ_Y6GkW3axrQWKXfXVsBEAbFv_I'
supabase: Client = create_client(supabase_url, supabase_key)

# Function to upload images to Supabase storage
def upload_to_supabase(filepath, bucket_name, folder_name, file_name):
    # Check if the file already exists in the bucket
    existing_files = supabase.storage.from_(bucket_name).list(folder_name)
    if file_name in [file['name'] for file in existing_files]:
        print(f"Skipping upload for {file_name} as it already exists.")
        return
    
    with open(filepath, 'rb') as f:
        supabase.storage.from_(bucket_name).upload(f"{folder_name}/{file_name}", f.read(), file_options={"content-type": "image/png"})

# Function to check if the anomaly already exists
def anomaly_exists(tic_id):
    match = re.search(r'\d+', tic_id)
    tic_id_numeric = int(match.group()) if match else None
    
    if tic_id_numeric is None:
        raise ValueError("TIC ID must contain a numeric value to be used as the anomaly ID.")
    
    response = supabase.table("anomalies").select("id").eq("id", tic_id_numeric).execute()
    return len(response.data) > 0

# Function to insert a new anomaly and get its ID
def insert_anomaly(tic_id):
    if anomaly_exists(tic_id):
        print(f"Anomaly for {tic_id} already exists. Skipping...")
        match = re.search(r'\d+', tic_id)
        tic_id_numeric = int(match.group()) if match else None
        return tic_id_numeric

    # Extract the numeric part of the TIC ID for use as the id
    match = re.search(r'\d+', tic_id)
    tic_id_numeric = int(match.group()) if match else None
    
    if tic_id_numeric is None:
        raise ValueError("TIC ID must contain a numeric value to be used as the anomaly ID.")

    configuration = {
        "mass": None,
        "ticId": tic_id,
        "radius": None,
        "smaxis": None,
        "ticId2": None,
        "density": None,
        "orbital_period": None,
        "temperature_eq": None
    }

    data = {
        "id": tic_id_numeric,  # Use the numeric part of the TIC ID as the primary key
        "content": tic_id,
        "ticId": tic_id,
        "anomalytype": "planet",
        "type": "unknown",
        "configuration": configuration
    }

    response = supabase.table("anomalies").upsert(data).execute()
    anomaly_id = response.data[0]['id']
    return anomaly_id

# Function to generate light curves and save plots
def generate_lightcurves(tic_id, output_dir):
    # Search for lightcurve data
    sector_data = lk.search_lightcurve(tic_id, author='SPOC')
    select_sector = sector_data[0:4]
    lc_collection = select_sector.download_all()

    # Plot individual light curves
    fig1, ax1 = plt.subplots()
    lc = select_sector.download_all()
    lc.plot(ax=ax1, linewidth=0, marker='.', markersize=1, color='midnightblue', alpha=0.3)
    fig1.savefig(os.path.join(output_dir, 'individual_light_curves.png'))
    plt.close(fig1)

    # Stitch the light curves
    lc_collection_stitched = lc_collection.stitch()
    fig2, ax2 = plt.subplots()
    lc_collection_stitched.plot(ax=ax2, linewidth=0, marker='.', markersize=1, color='midnightblue', alpha=0.3)
    fig2.savefig(os.path.join(output_dir, 'stitched_light_curves.png'))
    plt.close(fig2)

    # Bin the light curves with a larger bin time
    bin_time = 15 / 24 / 60  # 15-minute binning
    lc_collection_binned = lc_collection_stitched.bin(bin_time)
    fig3, ax3 = plt.subplots()
    lc_collection_binned.plot(ax=ax3, linewidth=0, marker='o', markersize=4, color='red', alpha=0.7)
    fig3.savefig(os.path.join(output_dir, 'binned_light_curves.png'))
    plt.close(fig3)

    # Plot stitched and binned light curves together
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    lc_collection_stitched.plot(ax=ax4, linewidth=0, marker='.', markersize=1, color='midnightblue', alpha=0.3, label='Unbinned')
    lc_collection_binned.plot(ax=ax4, linewidth=0, marker='o', markersize=4, color='red', alpha=0.7, label='Binned')
    ax4.legend()
    fig4.savefig(os.path.join(output_dir, 'stitched_and_binned_light_curves.png'))
    plt.close(fig4)

    # Zoom in on a specific time range to highlight transits
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    lc_collection_stitched.plot(ax=ax5, linewidth=0, marker='.', markersize=1, color='midnightblue', alpha=0.3, label='Unbinned')
    lc_collection_binned.plot(ax=ax5, linewidth=0, marker='o', markersize=4, color='red', alpha=0.7, label='Binned')
    ax5.set_xlim(lc_collection_stitched.time.min().value, lc_collection_stitched.time.min().value + 5)  # Adjust zoom range here
    ax5.legend()
    fig5.savefig(os.path.join(output_dir, 'zoomed_light_curves.png'))
    plt.close(fig5)

    # Apply a smoothing filter to the light curve
    smoothed_lc = lc_collection_stitched.flatten(window_length=301)
    fig6, ax6 = plt.subplots(figsize=(10, 5))
    smoothed_lc.plot(ax=ax6, linewidth=0, marker='.', markersize=1, color='midnightblue', alpha=0.3, label='Smoothed')
    fig6.savefig(os.path.join(output_dir, 'smoothed_light_curves.png'))
    plt.close(fig6)

# Main function
def main(tic_ids):
    output_dir = 'output'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for tic_id in tic_ids:
        if anomaly_exists(tic_id):
            print(f"Anomaly for {tic_id} already exists. Skipping...")
            continue

        anomaly_id = insert_anomaly(tic_id)
        anomaly_folder = str(anomaly_id)

        generate_lightcurves(tic_id, output_dir)
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                upload_to_supabase(file_path, 'anomalies', anomaly_folder, filename)

        print(f"Processed TIC ID {tic_id}, Anomaly ID: {anomaly_id}")

if __name__ == "__main__":
    tic_ids_list = ['TIC 50365310', 'TIC 88863718', 'TIC 124709665', 'TIC 106997505', 'TIC 238597883', 'TIC 169904935', 'TIC 156115721', 'TIC 65212867', 'TIC 440801822']
    main(tic_ids_list)
