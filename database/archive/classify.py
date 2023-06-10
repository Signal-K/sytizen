from flask import Flask, Blueprint, jsonify, request, Response
from .datastore import supabase, find_all_planets, add_planet_to_DB, planets
# from .app import app
# from views.models import Planet
# from .main import gen_image
# views.py
classify = Blueprint('classify', __name__)

# GET request -> return all planets in storage/db in JSON format
@classify.route('/planets')
def get_planets():
    planets = find_all_planets()
    return jsonify({
        'planets': planets, # Then present this on react frontend, port 5000 -> 3000
    })

@classify.route('/planets/<planet_id>')
def find_planet_by_id(planet_id):
    for planet in planets:
        if planet["id"] == int(planet_id):
            return jsonify({
                "planet": planet,
            })

@classify.route('/planets/add', methods=['POST'])
def add_planet():
    data = request.get_json()
    try:
        title = data['title']
        ticId = data['ticId']
        # Generate a static image
        # for seed in range(0, 10):
            # gen_image(seed)
            # return send_file('static/out0.png', mimetype='image/png')
            # Upload this image to supabase
            #"""axios.post('https://b4c251b4-c11a-481e-8206-c29934eb75da.deepnoteproject.com/planets/add', {
            #    get image from static/out0.png -> https://deepnote.com/workspace/star-sailors-49d2efda-376f-4329-9618-7f871ba16007/project/Star-Sailors-Light-Curve-Plot-b4c251b4-c11a-481e-8206-c29934eb75da/%2Fstatic%2Fout0.png. This is generated on Deepnote then...permanent URL
            #    Lightkurve -> https://deepnote.com/workspace/star-sailors-49d2efda-376f-4329-9618-7f871ba16007/project/Star-Sailors-Light-Curve-Plot-b4c251b4-c11a-481e-8206-c29934eb75da/%2Fstatic%2Flightcurve.fits
            #}).then(res => {
            #    set this as the url of the image. Still need to determine how to upload it to Supabase storage (could we link an IPFS when it's generated?)
            #    console.log('res', res.data);
            #}).catch(err => {
            #    console.log('error in request', err);
            #})
            #"""
        data = add_planet_to_DB(title, ticId)
        return jsonify(data), 201
    except:
        return Response('''{"message": "Bad Request"}''', status=400, mimetype='application/json')

@classify.route('/generator')
def generate():
    # Generate the figure **without using pyplot**.
    res = 2048 # see generate blueprint above
    """fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"""#"