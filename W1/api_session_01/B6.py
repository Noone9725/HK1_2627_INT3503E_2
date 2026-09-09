from flask import Flask, request, jsonify
app = Flask(__name__)

# Bộ đếm id tự tăng
_next_id = 4

# Database giả lập ban đầu
BOOKS = [
    {"id": 1, "title": "Book_1", "author": "Aut_1"},
    {"id": 2, "title": "Book_2", "author": "Aut_2"},
    {"id": 3, "title": "Book_3", "author": "Aut_3"},
]

# Tìm sách theo id
def find_book(bid):
    return next((b for b in BOOKS if b["id"] == bid), None)

# Get all list books 
@app.route("/books", methods=["GET"])
def list_books():
    limit = int(request.args.get("limit", 100))
    return jsonify(BOOKS[:limit]), 200

# Get book by id 
# Ép kiểu <int:> sẵn từ URL
@app.route("/books/<int:bid>", methods=["GET"])
def get_book(bid):
    book = find_book(bid)
    if not book:
        return jsonify({"error": "not found"}), 404
    return jsonify(book), 200

# Create new book
@app.route("/books", methods=["POST"])
def create_book():
    global _next_id
    body = request.get_json(silent=True) or {}
    title = body.get("title")
    author = body.get("author")

    # Validation bắt buộc có title và author
    if not title or not author:
        return jsonify({"error": "need title+author"}), 400

    new_book = {
        "id": _next_id,
        "title": title,
        "author": author,
    }
    BOOKS.append(new_book)
    _next_id += 1
    return jsonify(new_book), 201, {"Location": f"/books/{new_book['id']}"}

# Update (Put) & Delete book by id
@app.route("/books/<int:bid>", methods=["PUT", "DELETE"])
def modify_book(bid):
    book = find_book(bid)
    if not book:
        return jsonify({"error": "not found"}), 404

    # Update
    if request.method == "PUT":
        data = request.get_json(silent=True) or {}
        book["title"] = data.get("title", book["title"])
        book["author"] = data.get("author", book["author"])
        return jsonify(book), 200

    # Delete
    if request.method == "DELETE":
        BOOKS.remove(book)
        return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)