from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

@app.route('/api/posts', methods=['GET', 'POST'])
def get_add_posts():
    if request.method == 'POST':

        try:
            new_post = request.get_json()
            title = new_post.get('title')
            content = new_post.get('content')
            if not title or not content:
                raise ValueError('Missing title or content')

            new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
            POSTS.append({'id': new_id, 'title': title, 'content': content})

            return jsonify({"status": "success", "received": new_post}), 201
        except ValueError:
            return jsonify({"status": "error", "message": "Missing required fields: title and content"}), 400

    elif request.method == 'GET':
        return jsonify(POSTS)

@app.route('/api/posts/<int:id>', methods=['DELETE', 'PUT'])
def update_delete_posts(id):
    if request.method == 'PUT':
        try:
            update_data = request.get_json()
            if not update_data:
                raise ValueError('No data provided')

            title = update_data.get('title')
            content = update_data.get('content')
            if not title or not content:
                raise ValueError('Missing title or content')

            for post in POSTS:
                if post['id'] == id:
                    post.update(update_data)
                    return jsonify(post), 200
            return jsonify({"status": "error", "message": "Post not found"}), 404
        except ValueError:
            return jsonify({"status": "error", "message": "Missing required fields: title and content"}), 400

    elif request.method == 'DELETE':
        for post in POSTS:
            if post['id'] == id:
                POSTS.remove(post)
                return jsonify({"status": "success"}), 200
        return jsonify({"status": "error", "message": "Post not found"}), 404

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    search_key = request.args.get('key')
    query = request.args.get('query')

    if not query:
        return jsonify({"status": "error", "message": "Query parameter required"}), 400

    results = []

    if search_key == "title":
        results = [post for post in POSTS if query.lower() in post['title'].lower()]
    elif search_key == "content":
        results = [post for post in POSTS if query.lower() in post['content'].lower()]
    else:
        return jsonify({"status": "error", "message": "Invalid key"}), 400

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
