from supabase_py import create_client, Client
import subprocess

def fetch_entries_from_supabase(supabase: Client):
    # Fetch the entries from your Supabase table
    response = supabase.table('planetsss').select('*').execute()
    if 'error' in response:
        print(f"Error fetching entries: {response['error']}")
        return []
    return response['data']

# Initialize the Supabase client
url: str = "https://qwbufbmxkjfaikoloudl.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3YnVmYm14a2pmYWlrb2xvdWRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDE3NTksImV4cCI6MTk4NTUxNzc1OX0.RNz5bvsVwLvfYpZtUjy0vBPcho53_VS2AIVzT8Fm-lk"
supabase = create_client(url, key)

entries = fetch_entries_from_supabase(supabase)

for entry in entries:
    tic_id = entry['ticId']
    output_notebook = f"output/{tic_id}_notebook.ipynb"
    command = f"papermill master.ipynb {output_notebook} -p TIC '{tic_id}'"
    subprocess.run(command, shell=True)