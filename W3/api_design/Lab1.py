from flask import Flask, request, jsonify

app = Flask(__name__)

# Dữ liệu giả lập
posts_db = [
    {"id": 1, "title": "First Post", "content": "Hello World"}
]

@app.route('/api/v1/posts', methods=['GET'])
def get_posts():
    return jsonify(posts_db), 200

@app.route('/api/v1/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = {
        "id": len(posts_db) + 1,
        "title": data.get("title"),
        "content": data.get("content")
    }
    posts_db.append(new_post)
    return jsonify(new_post), 201

@app.route('/api/v1/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if post is None:
        return jsonify({"error": "Not Found"}), 404
    return jsonify(post), 200

@app.route('/api/v1/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if post is None:
        return jsonify({"error": "Not Found"}), 404
    
    data = request.get_json()
    post.update({
        "title": data.get("title", post["title"]),
        "content": data.get("content", post["content"])
    })
    return jsonify(post), 200

@app.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global posts_db
    initial_length = len(posts_db)
    posts_db = [p for p in posts_db if p["id"] != post_id]
    
    if len(posts_db) == initial_length:
        return jsonify({"error": "Not Found"}), 404
        
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)