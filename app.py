import os
from flask import Flask, jsonify
from supabase import create_client, Client
from pathlib import Path
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

SUPABASE_URL = 'http://127.0.0.1:54321'
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

def init_supabase_client():
    url = "http://127.0.0.1:54321"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
    return create_client(url, key)

supabase_client = init_supabase_client()

@app.route('/')
def hello_world():
    return 'Hello, World! Yay'

def upload_file_to_supabase(bucket_name: str, file_path: str, destination_path: str):
    with open(file_path, "rb") as file:
        try:
            response = supabase_client.storage.from_(bucket_name).upload(destination_path, file)
            print(f"Uploaded {file_path} -> {destination_path}")
            return True
        except Exception as e:
            print(f"Failed to upload {file_path} -> {destination_path}: {e}")
            return False

def upload_directory_to_supabase(bucket_name: str, local_directory: str):
    for root, dirs, files in os.walk(local_directory):
        for file_name in files:
            if file_name.startswith('.'):
                continue

            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, local_directory)
            destination_path = Path(relative_path).as_posix()

            success = upload_file_to_supabase(bucket_name, file_path, destination_path)
            if not success:
                return False
    return True

@app.route('/upload-directory', methods=['GET'])
def upload_directory():
    try:
        bucket_name = "zoodex"
        local_directory = "zoodex" 
        
        upload_success = upload_directory_to_supabase(bucket_name, local_directory)
        
        if upload_success:
            return jsonify({"message": "Directory uploaded successfully!"}), 200
        else:
            return jsonify({"message": "Failed to upload directory."}), 500
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/anomalies', methods=['GET'])
def get_anomalies():
    try:
        print("Attempting to fetch anomalies...")
        response = supabase_client.from_('anomalies').select('*').execute()
        
        
        if response.data:
            print(f"Supabase response: {response.data}") 
            return jsonify(response.data), 200
        else:
            print(f"No data found. Error: {response.error_message if response.error_message else 'Unknown error'}")
            return jsonify({"error": response.error_message or "No anomalies found"}), 404

    except Exception as e:
        print(f"An error occurred: {str(e)}") 
        return jsonify({"error": str(e)}), 500

def list_files_in_bucket(bucket_name: str):
    try:
        response = supabase_client.storage.from_(bucket_name).list()
        
    
        file_tree = {}
        
        for item in response.data:
            path_parts = item.name.split('/')
            current_level = file_tree
            
           
            for part in path_parts:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
        
        return file_tree
    
    except Exception as e:
        print(f"Error fetching files from bucket: {str(e)}")
        return {}
    
# @app.route('/buckets', methods=['GET'])
def list_files_in_bucket_zoodex():
    try:
    
        response = supabase_client.storage.from_("zoodex").list()
        
    
        file_tree = {}
        
    
        if isinstance(response, list):
            for item in response:
            
                path_parts = item['name'].split('/')
                current_level = file_tree
                
               
                for part in path_parts:
                    if part not in current_level:
                        current_level[part] = {}
                    current_level = current_level[part]
                    
            
                current_level['__file__'] = item['name'] 
                
    
        def clean_tree(tree):
            for key, value in list(tree.items()):
                if '__file__' in value:
                    
                    value['__file__'] = value['__file__']
                else:
                    
                    clean_tree(value)
                    
                    if not value:
                        del tree[key]

        clean_tree(file_tree)  
        
        return jsonify(file_tree)  
    
    except Exception as e:
        print(f"Error fetching files from bucket: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/buckets', methods=['GET'])
def list_files_in_burrowing_owl_folder():
    try:
        response = supabase_client.storage.from_("zoodex").list("zoodex-burrowingOwl/")
        files_list = [item['name'] for item in response if not item['name'].endswith('/')]
        return jsonify(files_list)
    except Exception as e:
        print(f"Error fetching files from bucket: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/list-files/<string:bucket_name>', methods=['GET'])
def list_files(bucket_name):
    try:
        file_tree = list_files_in_bucket(bucket_name)
        return jsonify(file_tree), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Supabase client initialized at startup")
    app.run(host='0.0.0.0', port=5001, debug=True)