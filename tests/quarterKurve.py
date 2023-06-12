from flask import flask
import lightkurve as lk
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"]) # in production/staging, this would not be the default route...
def index():
    if request.method == 'POST':
        tic_id = request.form['tic_id'] # Enter a tic id in the POST request
        tic_numerals = ''.join(filter(str.isdigit, tic_id)) # number of trees that will be generated
        lc = lk.search_lightcurve(tic_id, author="Kepler", quarter=3).download()
        lc.plot()
        # Save the plot as a bytes object
        image_bytes = BytesIO()
        plt.savefig(image_bytes, format='png')
        plt.close()
        image_bytes.seek(0)
        # Convert the bytes object to base64 string for embedding in HTML
        encoded_image = base64.b64encode(image_bytes.getvalue()).decode('utf-8')
        return render_template('result.html', image_data=encoded_image, tic_numerals=tic_numerals)
    return render_template('index.html')

@app.route('/send_tic_numerals', methods=['POST'])
def send_tic_numerals():
    tic_numerals = request.json['tic_numerals']
    return jsonify(message='TIC Numerals received by Flask')

if __name__ == '__main__':
    app.run()