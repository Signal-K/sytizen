from flask import Flask, request, render_template, jsonify
import lightkurve as lk
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import requests
import json

app = Flask(__name__)

def get_transit_parameters(tic_id):
    url = f"https://exofop.ipac.caltech.edu/tess/target.php?id={tic_id}" #download_single.php?exofop={tic_id}"
    response = requests.get(url)
    
    try:
        response.raise_for_status()
        data = response.json()
        
        # Extract the transit parameters from the response
        period = data["transitinfo"][0]["period"]
        t0 = data["transitinfo"][0]["T0"]
        
        return period, t0
    except requests.exceptions.HTTPError as e:
        error_message = f"HTTP Error: {e}"
    except json.JSONDecodeError as e:
        error_message = f"JSON Decode Error: {e}"
    except KeyError as e:
        error_message = f"Key Error: {e}"
    except Exception as e:
        error_message = str(e)
    
    # Print or log the error message for debugging
    print(f"Error retrieving transit parameters for TIC ID {tic_id}: {error_message}")
    
    # Return default values or handle the error condition as needed
    return None, None

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        tic_id = request.form['tic_id']
        tic_numerals = ''.join(filter(str.isdigit, tic_id))
        
        try:
            lc = lk.search_lightcurve(tic_id).download()
            lc.plot()
            # Save the plot as a bytes object
            image_bytes = BytesIO()
            plt.savefig(image_bytes, format='png')
            plt.close()
            image_bytes.seek(0)
            # Convert the bytes object to base64 string for embedding in HTML
            encoded_image = base64.b64encode(image_bytes.getvalue()).decode('utf-8')

            # Retrieve transit parameters from ExoFOP
            tic_numerals_exofop = ''.join(filter(str.isdigit, tic_id))  # Remove non-digit characters from the beginning of TIC ID
            period, t0 = get_transit_parameters(tic_numerals_exofop)

            return render_template('result.html', image_data=encoded_image, tic_numerals=tic_numerals, period=period, t0=t0)
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)
    
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/send_tic_numerals', methods=['POST'])
def send_tic_numerals():
    tic_numerals = request.json['tic_numerals']
    return jsonify(message='TIC Numerals received by Flask')

if __name__ == '__main__':
    app.run()