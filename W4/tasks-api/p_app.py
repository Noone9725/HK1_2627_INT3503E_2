from flask import Flask, request, jsonify

app = Flask(__name__)

# Database giả lập
# Bảng Book
books_db = [
    {"id": 1, "title": "Lập trình Python", "author_id": 101, "published_year": 2021},
    {"id": 2, "title": "Cấu trúc dữ liệu", "author_id": 102, "published_year": 2019},
    {"id": 3, "title": "API Design", "author_id": 101, "published_year": 2023},
    {"id": 4, "title": "Mạng máy tính", "author_id": 103, "published_year": 2020},
    {"id": 5, "title": "Cơ sở dữ liệu", "author_id": 101, "published_year": 2018}
]

# Bảng BookCopy phụ thuộc vào bảng Book (Quan hệ 1-N)
copies_db = [
    {"id": 1001, "book_id": 1, "barcode": "PY-001", "status": "available"},
    {"id": 1002, "book_id": 1, "barcode": "PY-002", "status": "borrowed"},
    {"id": 1003, "book_id": 2, "barcode": "DS-001", "status": "available"},
    {"id": 1004, "book_id": 3, "barcode": "API-001", "status": "lost"}
]

# Top-level Resource: Danh sách đầu sách (Hỗ trợ Lọc & Phân trang Offset)
@app.route('/v1/books', methods=['GET'])
def get_books():
    # Thực hiện Lọc (Filtering) qua Query Parameter
    author_id_filter = request.args.get('author_id')
    filtered_books = books_db
    if author_id_filter:
        try:
            author_id = int(author_id_filter)
            filtered_books = [book for book in filtered_books if book['author_id'] == author_id]
        except ValueError:
            return jsonify({"description": "author_id phải là số nguyên", "status": 400}), 400

    # Xử lý Phân trang (Offset Pagination)
    try:
        limit = int(request.args.get('limit', 2)) # Mặc định lấy 2 bản ghi
        offset = int(request.args.get('offset', 0)) # Mặc định bắt đầu từ 0
    except ValueError:
        return jsonify({"description": "limit và offset phải là số nguyên", "status": 400}), 400

    # Cắt mảng dữ liệu
    paginated_books = filtered_books[offset : offset + limit]

    return jsonify({
        "data": paginated_books,
        "metadata": {
            "total": len(filtered_books),
            "limit": limit,
            "offset": offset,
            "next_offset": offset + limit if (offset + limit) < len(filtered_books) else None
        }
    }), 200

# Nested Resource: Danh sách bản sao vật lý của MỘT đầu sách cụ thể
@app.route('/v1/books/<int:book_id>/copies', methods=['GET'])
def get_book_copies(book_id):
    # Kiểm tra đầu sách có tồn tại không
    book_exists = any(book['id'] == book_id for book in books_db)
    if not book_exists:
        return jsonify({"description": "Không tìm thấy đầu sách", "status": 404}), 404
        
    # Lấy các bản sao thuộc về book_id này (Không cần phân trang vì số lượng copy thường nhỏ)
    copies = [copy for copy in copies_db if copy['book_id'] == book_id]
    
    return jsonify({
        "book_id": book_id,
        "total_copies": len(copies),
        "data": copies
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)