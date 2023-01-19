from flask import Flask, request, make_response, jsonify, Blueprint
from thirdweb.types import LoginPayload
from thirdweb import ThirdwebSDK
from datetime import datetime, timedelta
import os

from auth.moralisHandler import moralis_handler
from auth.thirdwebHandler import thirdweb_handler
from contracts.planetDrop import planet_drop
from database.connection import database_connection

app = Flask(__name__)
app.register_blueprint(moralis_handler, url_prefix='/moralis-auth')
app.register_blueprint(thirdweb_handler, url_prefix='/auth')
app.register_blueprint(planet_drop, url_prefix='/planets')
app.register_blueprint(database_connection, url_prefix='/database')

@app.route('/')
def index():
    return "Hello World"

# Getting proposals route
#@app.route('/proposals')
#def getProposals():
#    return classifications;