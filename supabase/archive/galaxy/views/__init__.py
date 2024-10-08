from flask import Flask, Blueprint, jsonify, request, Response
from .datastore import supabase, find_all_planets, add_planet_to_DB, planets
# from .app import app
# from views.models import Planet

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