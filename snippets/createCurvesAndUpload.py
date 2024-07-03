import lightkurve as lk
import matplotlib.pyplot as plt
from supabase import create_client, Client

# Initialize Supabase client
supabase_url = 'https://hlufptwhzkpkkjztimzo.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsdWZwdHdoemtwa2tqenRpbXpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyOTk3NTUsImV4cCI6MjAzMTg3NTc1NX0.v_NDVWjIU_lJQSPbJ_Y6GkW3axrQWKXfXVsBEAbFv_I'
supabase: Client = create_client(supabase_url, supabase_key)

# Fetch anomalies with anomalytype 'planet'
anomalies_list = supabase.table("anomalies").select("id, configuration").eq("anomalytype", "planet").execute()

# Define a function to upload image to Supabase storage
def upload_to_supabase(filepath, bucket_name, folder_name, file_name):
    with open(filepath, 'rb') as f:
        supabase.storage.from_(bucket_name).upload(f"{folder_name}/{file_name}", f.read(), file_options={"content-type": "image/png"})

# Process each anomaly
for anomaly in anomalies_list.data:
    anomaly_id = anomaly['id']
    config = anomaly['configuration']
    tic_id = config['ticId']

    # Define TIC and other parameters from the configuration
    TIC = tic_id
    period = config.get('orbital_period', 13)
    t0 = 303  # You may need to adjust this value as per your requirements

    # Search and download lightcurve data
    sector_data = lk.search_lightcurve(TIC)
    lc = sector_data.download()

    # Plot original lightcurve and save as 'base.png'
    fig, ax = plt.subplots()
    lc.plot(ax=ax, color='blue', marker='.', lw=0)
    plt.savefig('base.png', format='png')
    upload_to_supabase('base.png', 'anomalies', str(anomaly_id), 'base.png')
    plt.show()

    # Bin the lightcurve data and save as 'binned.png'
    bin_time = 15 / 24 / 60
    lc_binned = lc.bin(bin_time)
    fig, ax = plt.subplots()
    lc_binned.plot(ax=ax, color='gold', lw=0, marker='.')
    plt.savefig('binned.png', format='png')
    upload_to_supabase('binned.png', 'anomalies', str(anomaly_id), 'binned.png')
    plt.show()

    # Fold the lightcurve and save as 'phased.png'
    lc_phased = lc.fold(period=period, epoch_time=t0)
    fig, ax = plt.subplots(figsize=(8, 4))
    lc_phased.plot(ax=ax, linewidth=0, marker='o', color='pink', markersize=1, alpha=0.8)
    plt.savefig('phased.png', format='png')
    upload_to_supabase('phased.png', 'anomalies', str(anomaly_id), 'phased.png')
    plt.show()
