import os
from supabase import create_client, Client

def init_supabase_client():
    url = "http://127.0.0.1:54321"  
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
    return create_client(url, key)

def fetch_anomalies(supabase: Client):
    response = supabase.table('anomalies').select("*").execute()
    return response.data

def fetch_classifications(supabase: Client):
    # Explicitly select classificationtype and other fields
    response = supabase.table('classifications').select("id, content, anomaly, classificationtype, classificationConfiguration").execute()
    return response.data

def group_anomalies_by_type(anomalies, classifications):
    # Extract anomaly IDs from classifications
    classified_anomaly_ids = {classification['anomaly'] for classification in classifications if classification['anomaly']}
    
    # Group anomalies by their type and include classifications
    grouped_anomalies = {}
    for anomaly in anomalies:
        anomaly_id = anomaly['id']
        if anomaly_id in classified_anomaly_ids:
            anomaly_type = anomaly['anomalytype']
            if anomaly_type not in grouped_anomalies:
                grouped_anomalies[anomaly_type] = {'anomalies': [], 'classifications': []}
            grouped_anomalies[anomaly_type]['anomalies'].append(anomaly)
            # Add all classifications for this anomaly
            for classification in classifications:
                if classification['anomaly'] == anomaly_id:
                    grouped_anomalies[anomaly_type]['classifications'].append(classification)

    return grouped_anomalies

def extract_planet_anomalies(anomalies):
    return [anomaly for anomaly in anomalies if anomaly['anomalytype'] == "planet"]

def export_to_txt(grouped_anomalies, planet_anomalies, filename='anomalies_grouped.txt'):
    with open(filename, 'w') as file:
        # Write grouped anomalies
        for anomaly_type, data in grouped_anomalies.items():
            file.write(f"Anomaly Type: {anomaly_type}\n")
            for anomaly in data['anomalies']:
                file.write(f"  - ID: {anomaly['id']}, Content: {anomaly['content']}\n")
                # Write associated classifications
                classifications = data['classifications']
                if classifications:
                    file.write("    Classifications:\n")
                    for classification in classifications:
                        file.write(f"      * ID: {classification['id']}, Content: {classification['content']}, ")
                        file.write(f"Type: {classification['classificationtype']}, ")
                        file.write(f"ClassificationConfig: {classification['classificationConfiguration']}\n")
            file.write("\n")
        
        # Write planet anomalies
        file.write("Anomalies of Type: planet\n")
        for anomaly in planet_anomalies:
            file.write(f"  - ID: {anomaly['id']}, Content: {anomaly['content']}\n")
        file.write("\n")
    
    print(f"Data exported to {filename}")

def main():
    supabase = init_supabase_client()
    
    # Fetch data from Supabase
    anomalies = fetch_anomalies(supabase)
    classifications = fetch_classifications(supabase)
    
    # Group anomalies
    grouped_anomalies = group_anomalies_by_type(anomalies, classifications)
    
    # Extract planet anomalies
    planet_anomalies = extract_planet_anomalies(anomalies)
    
    # Export results to a text file
    export_to_txt(grouped_anomalies, planet_anomalies)

if __name__ == "__main__":
    main()