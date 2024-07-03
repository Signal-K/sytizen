import pandas as pd
from supabase import create_client, Client

# Initialize Supabase client
supabase_url = 'https://hlufptwhzkpkkjztimzo.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsdWZwdHdoemtwa2tqenRpbXpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyOTk3NTUsImV4cCI6MjAzMTg3NTc1NX0.v_NDVWjIU_lJQSPbJ_Y6GkW3axrQWKXfXVsBEAbFv_I'
supabase: Client = create_client(supabase_url, supabase_key)

# Fetch all anomalies with configuration data
anomalies_response = supabase.table("anomalies").select("id, configuration").execute()

# Filter anomalies with non-null configurations
anomalies = [anomaly for anomaly in anomalies_response.data if anomaly['configuration'] is not None]

# Create a list to store the results
results = []

# Process each anomaly
for anomaly in anomalies:
    anomaly_id = anomaly['id']
    configuration = anomaly['configuration']

    # Get classification types from configuration keys
    classification_types = configuration.keys()

    # Fetch classifications for the current anomaly with matching classification types
    classifications_response = supabase.table("classifications").select("id, anomaly, content, created_at").eq("anomaly", anomaly_id).execute()

    # Process each classification
    for classification in classifications_response.data:
        content = classification['content']

        # Check if classification type matches any configuration key
        for classification_type in classification_types:
            if classification_type in content:
                try:
                    value = float(content[classification_type])
                    results.append({
                        'anomaly': anomaly_id,
                        'classificationtype': classification_type,
                        'value': value
                    })
                except ValueError:
                    print(f"Skipping non-numeric classification for anomaly {anomaly_id}: {classification_type}={content[classification_type]}")

# Debug: print results
print("Results:", results)

# Convert results to a DataFrame if there are any results
if results:
    df = pd.DataFrame(results)
    # Debug: print DataFrame
    print("DataFrame:", df)

    # Group by anomaly and classificationtype, and calculate the average value
    averaged_results = df.groupby(['anomaly', 'classificationtype']).agg({'value': 'mean'}).reset_index()

    # Print the averaged results
    print("Averaged Results:", averaged_results)

    # Function to update anomaly configurations with averaged values
    def update_anomaly_configurations(averaged_results):
        for _, row in averaged_results.iterrows():
            anomaly_id = row['anomaly']
            classificationtype = row['classificationtype']
            avg_value = row['value']
            
            # Fetch the current configuration for the anomaly
            anomaly_response = supabase.table("anomalies").select("configuration").eq("id", anomaly_id).execute()
            if anomaly_response.data:
                configuration = anomaly_response.data[0]['configuration']
                # Update the configuration with the averaged value
                configuration[classificationtype] = avg_value
                
                # Update the anomaly configuration in the database
                supabase.table("anomalies").update({'configuration': configuration}).eq("id", anomaly_id).execute()

    # Update anomaly configurations with the averaged values
    update_anomaly_configurations(averaged_results)
else:
    print("No valid results to process.")