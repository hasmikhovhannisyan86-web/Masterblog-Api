from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post",
     "content": "This is the second post."},
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
            new_id = max(p['id'] for p in POSTS) + 1 if POSTS else 1
            post = {'id': new_id, 'title': title, 'content': content}
            POSTS.append(post)
            return jsonify(post), 201
        except ValueError:
            msg = "Missing required fields: title and content"
            return jsonify({"status": "error", "message": msg}), 400
    return jsonify(POSTS)


@app.route('/api/posts/<int:id>', methods=['DELETE', 'PUT'])
def update_delete_posts(id):
    if request.method == 'PUT':
        update_data = request.get_json()
        if not update_data:
            return jsonify({"status": "error",
                            "message": "No data provided"}), 400
        for post in POSTS:
            if post['id'] == id:
                post['title'] = update_data.get('title', post['title'])
                post['content'] = update_data.get(
                    'content', post['content'])
                return jsonify(post), 200
        return jsonify({"status": "error",
                        "message": "Post not found"}), 404
    elif request.method == 'DELETE':
        for post in POSTS:
            if post['id'] == id:
                POSTS.remove(post)
                msg = f"Post with id {id} has been deleted successfully."
                return jsonify({"message": msg}), 200
        return jsonify({"status": "error",
                        "message": "Post not found"}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title')
    content_query = request.args.get('content')
    results = POSTS
    if title_query:
        results = [
            p for p in results
            if title_query.lower() in p['title'].lower()
        ]
    if content_query:
        results = [
            p for p in results
            if content_query.lower() in p['content'].lower()
        ]
    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
