import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory storage for posts
posts = []

# Endpoint for creating a new post
@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    # Generate a unique ID for the post
    post_id = str(uuid.uuid4())

    post = {
        'id': post_id,
        'author': data['author'],
        'content': data['content'],
        'published': datetime.now().isoformat()
    }

    posts.append(post)

    # Return the created post
    return jsonify({'id': post_id})

# Endpoint for retrieving all posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify({'posts': posts})

if __name__ == '__main__':
    app.run(debug=True)

"""
import uuid
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for posts
posts = []

# Generate a unique actor ID
actor_id = str(uuid.uuid4())

# Generate a unique actor URL based on the actor ID
actor_url = f"http://your-domain.com/actors/{actor_id}"

# Endpoint for creating a new post
@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    # Generate a unique ID for the post
    post_id = str(uuid.uuid4())

    post = {
        'id': post_id,
        'actor': actor_url,
        'content': data['content'],
        'published': datetime.now().isoformat()
    }

    posts.append(post)

    # Return the created post
    return jsonify({'id': post_id, 'url': f"http://your-domain.com/posts/{post_id}"}), 201

# Endpoint for retrieving all posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify({'posts': posts})

if __name__ == '__main__':
    app.run(debug=True)
"""