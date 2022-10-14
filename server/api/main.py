from flask import Flask, request, Blueprint, render_template
#from .TIC_Page import TIC_page

app = Flask(__name__)
app.register_blueprint(TIC_Page)