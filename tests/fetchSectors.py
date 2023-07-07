from flask import Flask, render_template, request
from lightkurve import search_targetpixelfile

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        tic_id = request.form['tic_id']
        try:
            search_result = search_targetpixelfile(tic_id, mission='TESS')
            tpf = search_result.download(quality_bitmask='default')
            sectors = tpf.meta.get('SECTOR', [])
            authors = tpf.meta.det('AUTHOR', '')
            tpf.plot()
            return render_template('sectorResult.html', sectors=sectors, authors=authors)

        except Exception as e:
            error = str(e)
            return render_template('sectorIndex.html', error=error)
    
    return render_template('sectorIndex.html')

if __name__ == '__main__':
    app.run(debug=True)