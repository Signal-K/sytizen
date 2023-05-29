from flask import Flask, render_template, Blueprint, jsonify
import lightkurve as lk
import os
from supabase import create_client

"""# Flask blueprints ""
from database.classify import classify
from views.lightkurve import lightkurve_bp"""

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world"