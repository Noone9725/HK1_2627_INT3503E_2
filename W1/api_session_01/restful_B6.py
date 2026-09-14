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

# 1. Bắt lỗi Content-Type toàn cục (415)
@app.before_request
def check_content_type():
    if request.method in ["POST", "PUT", "PATCH"]:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415

# 2. LIST & SEARCH & SORT (GET)
@app.route("/books", methods=["GET"])
def list_books():
    q = request.args.get("q", "").strip().lower()
    sort_by = request.args.get("sort", "").strip().lower()

    result = [b for b in BOOKS if q in b["title"].lower()]
    if sort_by == "title":
        result.sort(key=lambda x: x["title"].lower())

    return jsonify(result), 200

# 3. DETAIL (GET)
@app.route("/books/<int:bid>", methods=["GET"])
def get_book(bid):
    book = find_book(bid)
    if not book:
        return jsonify({"error": "not found"}), 404
    return jsonify(book), 200

# 4. CREATE (POST)
@app.route("/books", methods=["POST"])
def create_book():
    global _next_id
    body = request.get_json(silent=True)
    
    if body is None:
        return jsonify({"error": "Invalid JSON format"}), 400
        
    title = body.get("title")
    author = body.get("author")
    year = body.get("year")

    if not title or not author or year is None:
        return jsonify({"error": "need title+author+year"}), 400
    
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

# 5. FULL UPDATE (PUT)
@app.route("/books/<int:bid>", methods=["PUT"])
def update_book_full(bid):
    book = find_book(bid)
    if not book:
        return jsonify({"error": "not found"}), 404

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid JSON format"}), 400

    title = body.get("title")
    author = body.get("author")
    year = body.get("year")

    # PUT yêu cầu gửi ĐẦY ĐỦ các trường
    if not title or not author or year is None:
        return jsonify({"error": "PUT requires all fields: title, author, year"}), 400
        
    if type(year) is not int or year < 1900:
        return jsonify({"error": "year must be an integer >= 1900"}), 400

    book["title"] = title
    book["author"] = author
    book["year"] = year
    return jsonify(book), 200

# 6. PARTIAL UPDATE (PATCH)
@app.route("/books/<int:bid>", methods=["PATCH"])
def update_book_partial(bid):
    book = find_book(bid)
    if not book:
        return jsonify({"error": "not found"}), 404

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Invalid JSON format"}), 400

    # PATCH chỉ cập nhật trường nào được gửi lên
    if "title" in body:
        book["title"] = body["title"]
    if "author" in body:
        book["author"] = body["author"]
    if "year" in body:
        year = body["year"]
        if type(year) is not int or year < 1900:
            return jsonify({"error": "year must be an integer >= 1900"}), 400
        book["year"] = year

    return jsonify(book), 200

# 7. DELETE (DELETE)
@app.route("/books/<int:bid>", methods=["DELETE"])
def delete_book(bid):
    book = find_book(bid)
    if not book:
        return jsonify({"error": "not found"}), 404

    BOOKS.remove(book)
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)