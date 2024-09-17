from flask import Flask
from flask_cors import CORS
import uuid
from datetime import datetime

from tests.quarterKurve import quarterKurve_bp
from tests.lightKurve import lightKurve_bp
from auth.federated import federated_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(quarterKurve_bp, url_prefix='/quarterkurve')
app.register_blueprint(lightKurve_bp, url_prefix='/lightkurve')
app.register_blueprint(federated_bp, url_prefix='/federated')

if __name__ == '__main__':
    app.run(debug=True)