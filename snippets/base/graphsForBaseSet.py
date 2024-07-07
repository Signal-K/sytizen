import os
import shutil
import lightkurve as lk
import matplotlib.pyplot as plt
from supabase import create_client, Client

# Initialize Supabase client
supabase_url = 'https://hlufptwhzkpkkjztimzo.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsdWZwdHdoemtwa2tqenRpbXpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyOTk3NTUsImV4cCI6MjAzMTg3NTc1NX0.v_NDVWjIU_lJQSPbJ_Y6GkW3axrQWKXfXVsBEAbFv_I'
supabase: Client = create_client(supabase_url, supabase_key)

# Define the local folder path to save files
local_folder = './graphs'

# Function to upload images to Supabase storage
def upload_to_supabase(filepath, bucket_name, folder_name, file_name):
    # Check if the file already exists in the bucket
    existing_files = supabase.storage.from_(bucket_name).list(folder_name)
    if file_name in [file['name'] for file in existing_files]:
        print(f"Skipping upload for {file_name} as it already exists.")
        return
    
    with open(filepath, 'rb') as f:
        supabase.storage.from_(bucket_name).upload(f"{folder_name}/{file_name}", f.read(), file_options={"content-type": "image/png"})

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

# Function to process each TIC ID, generate graphs, and upload to Supabase
def process_and_upload(tic_id, anomaly_id):
    output_dir = os.path.join(local_folder, str(anomaly_id))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generate_lightcurves(tic_id, output_dir)

    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path):
            upload_to_supabase(file_path, 'anomalies', str(anomaly_id), filename)

    print(f"Processed TIC ID {tic_id}, Anomaly ID: {anomaly_id}")

# Main function
def main():
    tic_ids = ['KIC 8692861', 'KIC 8120608', 'KIC 4138008', 'KIC 10593636', 'EPIC 246199087', 'TIC 150428135']
    anomaly_ids = [1, 2, 3, 4, 5, 6]

    if os.path.exists(local_folder):
        shutil.rmtree(local_folder)
    os.makedirs(local_folder)

    for tic_id, anomaly_id in zip(tic_ids, anomaly_ids):
        process_and_upload(tic_id, anomaly_id)

if __name__ == "__main__":
    main()
