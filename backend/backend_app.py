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

            POSTS.append({'id': len(POSTS) + 1, 'title': title, 'content': content})

            return jsonify({"status": "success", "received": new_post}), 201
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    elif request.method == 'GET':
        return jsonify(POSTS)
    return None

@app.route('/api/posts/<int:id>', methods=['DELETE', 'PUT'])
def update_delete_posts(id):
    if request.method == 'PUT':
        for post in POSTS:
            if post['id'] == id:
                post.update(request.get_json())
                return jsonify(post), 200
        return jsonify({"status": "error", "message": "Post not found"}), 404

    elif request.method == 'DELETE':
        for post in POSTS:
            if post['id'] == id:
                POSTS.remove(post)
                return jsonify({"status": "success"}), 200
        return jsonify({"status": "error", "message": "Post not found"}), 404

@app.route('/api/posts/search', methods=['get'])
def search_posts():
    for post in POSTS:
        if request.args.get('key') == "title":
            for post in POSTS:
                if post['title'].lower().find(request.args.get('query').lower()) != -1:
                    return jsonify(post)
        elif request.args.get('key') == "content":
            for post in POSTS:
                if post['content'].lower().find(request.args.get('query').lower()) != -1:
                    return jsonify(post)
        else:
            return jsonify({"status": "error", "message": "Invalid key"}), 400
    return jsonify({}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
