from flask import Flask, render_template, request
from lightkurve import TessTargetPixelFile

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        tic_id = request.form['tic_id']
        try:
            tpf = TessTargetPixelFile.from_archive(tic_id, exptime=1800)
            sectors = tpf.sector
            authors = tpf.meta['AUTHORS']
            tpf.plot()
            return render_template('sectorResult.html', sectors=sectors, authors=authors)

        except Exception as e:
            error = str(e)
            return render_template('sectorIndex.html', error=error)
    
    return render_template('sectorIndex.html')

if __name__ == '__main__':
    app.run(debug=True)