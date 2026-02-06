from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':

        try:
            new_post = request.get_json()
            title = new_post.get('title')
            content = new_post.get('content')
            if not title or not content:
                raise ValueError('Missing title or content')

            POSTS.append({'id': len(POSTS) + 1, 'title': title, 'content': content})

            return jsonify({"status": "success", "received": new_post}), 201
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    elif request.method == 'GET':
        return jsonify(POSTS)
    return None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
