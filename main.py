from flask import Flask, jsonify
from models.planets import planets

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({
        'greeting': 'Hello World!'
    })

@app.route('/planets')
def get_planets():
    return jsonify({
        'planets': planets, # Then present this on react frontend, port 5000 -> 3000
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)