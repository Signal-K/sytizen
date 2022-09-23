from flask import Flask, request, render_template, jsonify
import lightkurve as lk
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def calculate_number_of_trees(amplitude):
    # Set the thresholds and corresponding number of trees
    thresholds = [0.1, 0.5, 1.0]  # Adjust these values as needed
    num_trees = [10, 5, 1]  # Adjust these values as needed

    # Find the corresponding number of trees based on the amplitude
    for i, threshold in enumerate(thresholds):
        if amplitude < threshold:
            return num_trees[i]

    # If the amplitude is above the highest threshold, return the lowest number of trees
    return num_trees[-1]

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        tic_id = request.form['tic_id']
        
        try:
            lc = lk.search_lightcurve(tic_id).download()
            flux = lc.flux
            amplitude = max(flux) - min(flux)
            
            # Calculate the number of trees based on the amplitude
            num_trees = calculate_number_of_trees(amplitude)

            # Add the number of trees to the amplitude as an indicator of habitability
            habitability = num_trees + amplitude

            return render_template('result.html', tic_id=tic_id, amplitude=amplitude, num_trees=num_trees, habitability=habitability)
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)
    
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html')


def get_transit_parameters(tic_id):
    url = f"https://exo.mast.stsci.edu/api/v0.1/exoplanets/identifiers/"
    payload = {
        "input": tic_id,
        "columns": "t0, period"
    }
    response = requests.get(url, params=payload)
    
    try:
        response.raise_for_status()
        data = response.json()
        
        # Extract the transit parameters from the response
        if data["data"]:
            period = data["data"][0]["period"]
            t0 = data["data"][0]["t0"]
            return period, t0
        
        # Handle the case when data is not available for the TIC ID
        error_message = f"No transit parameters available for TIC ID {tic_id}"
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

@app.route('/tic', methods=["GET", "POST"])
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

            # Retrieve transit parameters from the NASA Exoplanet Archive API
            period, t0 = get_transit_parameters(tic_id)

            return render_template('result1.html', image_data=encoded_image, tic_numerals=tic_numerals, period=period, t0=t0)
        
        except Exception as e:
            error_message = str(e)
            return render_template('error1.html', error_message=error_message)
    
    return render_template('index1.html')

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run()