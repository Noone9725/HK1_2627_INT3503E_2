from flask import Flask, jsonify, request
app = Flask(__name__)

# Database giả lập
BOOKS = [
    {"id": 1, "title": "Book_1", "author": "Aut_1"},
    {"id": 2, "title": "Book_2", "author": "Aut_2"},
    {"id": 3, "title": "Book_3", "author": "Aut_3"},
]

# 1. Path params 
# id là string
@app.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    # Nếu ép kiểu <int:> sẵn từ URL thì sẽ phức tạp hơn khi lấy báo lỗi JSON thay vì HTML, nên để string và check thủ công
    if not book_id.isdigit():
        return jsonify({"error": "id phai la so nguyen"}), 404

    book = next((b for b in BOOKS if b["id"] == int(book_id)), None)
    if book is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(book), 200

# 2. Query string
@app.route("/books", methods=["GET"])
def list_books():
    limit = int(request.args.get("limit", 20))
    q = request.args.get("q", "").strip().lower()
    items = [b for b in BOOKS if q in b["title"].lower()]
    return jsonify({"items": items[:limit]}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)