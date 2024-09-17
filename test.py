from flask import Flask, request, send_file
import lightkurve as lk
import matplotlib.pyplot as plt
from io import BytesIO
import asyncio

app = Flask(__name__)

async def fetch_lightcurve(tic_id):
    try:
        # Search for the lightcurve using search_lightcurve() instead of deprecated search_lightcurvefile()
        lc = lk.search_lightcurve("TIC " + tic_id).download_all().PDCSAP_FLUX.normalize().flatten(window_length=301).to_lightcurve()
        
        plt.figure(figsize=(10, 5))
        lc.plot()
        plt.title(f'Lightcurve for TIC ID {tic_id}')
        plt.xlabel('Time (days)')
        plt.ylabel('Normalized Flux')

        img_bytes = BytesIO()
        plt.savefig(img_bytes, format='png')
        img_bytes.seek(0)
        
        plt.close()
        
        return img_bytes
    except Exception as e:
        print(f"Error fetching lightcurve for TIC ID {tic_id}: {str(e)}")
        return None

@app.route('/lightcurve', methods=['GET'])
def get_lightcurve():
    tic_id = request.args.get('tic_id')

    if not tic_id:
        return "Error: Please provide a TIC ID in the 'tic_id' query parameter.", 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    img_bytes = loop.run_until_complete(fetch_lightcurve(tic_id))
    
    if img_bytes:
        return send_file(img_bytes, mimetype='image/png')
    else:
        return f"Error fetching lightcurve for TIC ID {tic_id}", 500

if __name__ == '__main__':
    app.run(debug=True)
