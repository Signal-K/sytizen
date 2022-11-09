from main import create_app, db
from models import Articles, article_schema, articles_schema
from flask import request, redirect, jsonify

app = create_app() # create application instance

@app.route("/articles", methods=["GET"], strict_slashes = False) # Route to collect (articles) data
def articles():
    articles = Articles.query.all()
    results = articles_schema.dump(articles) # Serialise data objects with dump method (returns structured result with marshmallow)
    return jsonify(results) # Response object with type app/json

if __name__ == "__main__":
    app.run(debug = True)