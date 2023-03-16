from flask import Flask, Blueprint, jsonify
# from .app import app
# from views.models import Planet

# views.py
main = Blueprint('main', __name__)

@main.route('/planet', methods=['GET', 'POST'])
def index():
    return jsonify(planets)

@main.route('/time')
def get_current_time():
    return {'time': time.time()}

# GET request -> return all planets in storage/db in JSON format
@main.route('/planets')
def get_planets():
    return jsonify({
        'planets': planets, # Then present this on react frontend, port 5000 -> 3000
    })

@main.route('/planets/<planet_id>')
def find_planet_by_id(planet_id):
    for planet in planets:
        if planet["id"] == int(planet_id):
            return jsonify({
                "planet": planet,
            })

@main.route('/planets/add', methods=['POST'])
def add_planet():
    data = request.get_json()
    try:
        title = data['title']
        if title:
            data = add_planet_to_DB(title)
            return jsonify(data), 201
    except:
        return Response('''{"message": "Bad Request"}''', status=400, mimetype='application/json')

@main.route('/generator')
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