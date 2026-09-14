from flask import Flask, jsonify, request
app = Flask(__name__)

# Bộ đếm id tự tăng
_next_id = 4

# Database giả lập ban đầu
BOOKS = [
    {"id": 1, "title": "Book_1", "author": "Aut_1", "year": 2010},
    {"id": 2, "title": "Book_2", "author": "Aut_2", "year": 2012},
    {"id": 3, "title": "Book_3", "author": "Aut_3", "year": 2015},
]

# Tìm sách theo id
def find_book(bid):
    return next((b for b in BOOKS if b["id"] == bid), None)

# LIST & SEARCH & SORT: GET /books
@app.route("/books", methods=["GET"])
def list_books():
    # Lấy query params
    q = request.args.get("q", "").strip().lower()
    sort_by = request.args.get("sort", "").strip().lower()

    # (a) Lọc theo q (nếu q rỗng thì lấy tất cả)
    result = [b for b in BOOKS if q in b["title"].lower()]

    # (b) Sắp xếp theo sort=title
    if sort_by == "title":
        # Hàm sort() sắp xếp trực tiếp trên list result
        result.sort(key=lambda x: x["title"].lower())

    return jsonify(result), 200

# DETAIL: GET /books/<id>
@app.route("/books/<int:bid>", methods=["GET"])
def get_book(bid):
    book = find_book(bid)
    if not book:
        return jsonify({"error": "not found"}), 404
    return jsonify(book), 200

# CREATE: POST /books
@app.route("/books", methods=["POST"])
def create_book():
    global _next_id
    body = request.get_json(silent=True) or {}
    title = body.get("title")
    author = body.get("author")
    year = body.get("year")

    # Validate bắt buộc có title & author & year
    if not title or not author or year is None:
        return jsonify({"error": "need title+author+year"}), 400
    
    # (c) Validate field year (phải là số nguyên >= 1900)
    if type(year) is not int or year < 1900:
        return jsonify({"error": "year must be an integer >= 1900"}), 400

    new_book = {
        "id": _next_id,
        "title": title,
        "author": author,
        "year": year
    }
    
    _next_id += 1
    BOOKS.append(new_book)
    return jsonify(new_book), 201, {"Location": f"/books/{new_book['id']}"}

# UPDATE & DELETE: /books/<id>
@app.route("/books/<int:bid>", methods=["PUT", "DELETE"])
def modify_book(bid):
    book = find_book(bid)
    if not book:
        return jsonify({"error": "not found"}), 404

    # Update
    if request.method == "PUT":
        data = request.get_json(silent=True) or {}
        
        # Nếu client gửi lên trường year, tiến hành validate
        if "year" in data:
            year = data["year"]
            if type(year) is not int or year < 1900:
                return jsonify({"error": "year must be an integer >= 1900"}), 400
            book["year"] = year

        book["title"] = data.get("title", book["title"])
        book["author"] = data.get("author", book["author"])
        return jsonify(book), 200

    # Delete
    if request.method == "DELETE":
        BOOKS.remove(book)
        return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)