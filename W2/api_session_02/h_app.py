# Homework B1: 
# Database SQLite. 
# Các endpoint (GET, POST, PUT, PATCH, DELETE) thực thi SQL code
# Endpoint GET /orders/ truy vấn bảng orders, trả về danh sách order và tổng số order
import sqlite3
import json
import hashlib
from flask import Flask, jsonify, request, make_response, g

app = Flask(__name__)
DATABASE = 'data.db'
DEFAULT_SIZE, MAX_SIZE = 20, 100

# Kết nối database SQLite và lưu trữ trong context của Flask
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Đóng kết nối database khi ứng dụng Flask kết thúc
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Tự động tạo bảng và seed dữ liệu nếu chưa có
def init_db():
    with app.app_context():
        db = get_db()
        # Bảng books
        db.execute('''CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        price REAL,
                        isbn TEXT
                      )''')
        # Bảng orders
        db.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_name TEXT NOT NULL,
                        quantity INTEGER NOT NULL
                      )''')
        
        # Seed data nếu bảng books trống
        cur = db.execute('SELECT COUNT(*) FROM books')
        if cur.fetchone()[0] == 0:
            initial_books = [
                ("Clean Code", "R. Martin", 25.5),
                ("Clean Architecture", "R. Martin", 28.0),
                ("1984", "Orwell", 15.0)
            ]
            db.executemany('INSERT INTO books (title, author, price) VALUES (?, ?, ?)', initial_books)
        db.commit()

init_db()

# GET /books/<id>: Lấy chi tiết sách theo id
@app.get("/books/<int:bid>")
def fetch(bid):
    db = get_db()
    book = db.execute('SELECT * FROM books WHERE id = ?', (bid,)).fetchone()
    if book is None: return jsonify(error="not found"), 404
    
    resp = make_response(jsonify(dict(book)), 200)
    resp.headers["Cache-Control"] = "max-age=60"
    return resp

# GET /books: Lấy danh sách sách với phân trang, lọc theo author và tìm kiếm theo title
@app.get("/books")
def list_books():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify(error="page and size must be int"), 400
    page = max(page, 1) 
    size = max(min(size, MAX_SIZE), 1)

    db = get_db()
    query = 'SELECT * FROM books WHERE 1=1'
    params = []

    a = request.args.get("author")
    if a:
        query += ' AND LOWER(author) = ?'
        params.append(a.lower())
    
    q = request.args.get("q")
    if q:
        query += ' AND LOWER(title) LIKE ?'
        params.append(f'%{q.lower()}%')

    total = db.execute(f'SELECT COUNT(*) FROM ({query})', params).fetchone()[0]
    
    query += ' LIMIT ? OFFSET ?'
    params.extend([size, (page-1) * size])
    
    items = [dict(row) for row in db.execute(query, params).fetchall()]
    last = (total + size - 1) // size

    def u(p): return f"/books?page={p}&size={size}"
    links = {
        "self": {"href": u(page)},
        "first": {"href": u(1)},
        "last": {"href": u(max(last, 1))}
    }
    if page > 1: links["prev"] = {"href": u(page-1)}
    if (page * size) < total: links["next"] = {"href": u(page+1)}

    body = {
        "data": items,
        "pagination": {"page": page, "size": size, "total": total, "total_pages": last},
        "_links": links
    }

    # Implement B3: ETag
    # Biến body thành chuỗi bytes
    response_bytes = json.dumps(body, sort_keys=True).encode('utf-8')
    
    # Tạo mã băm MD5 làm ETag
    etag = hashlib.md5(response_bytes).hexdigest()

    # Kiểm tra header If-None-Match từ client gửi lên
    if request.headers.get('If-None-Match') == etag:
        return "", 304

    # Nếu không khớp, trả về 200 kèm body và gắn ETag vào header
    resp = make_response(jsonify(body), 200)
    resp.headers["Cache-Control"] = "public, max-age=30"
    resp.set_etag(etag)
    return resp

# POST /books: Tạo mới sách
@app.post("/books")
def create_book():
    if not request.is_json: return jsonify(error="expected JSON"), 415
    p = request.get_json(silent=True) or {}
    t = (p.get("title") or "").strip()
    a = (p.get("author") or "").strip()
    if not t or not a: return jsonify(error="title and author required"), 422

    db = get_db()
    cur = db.execute('INSERT INTO books (title, author, price, isbn) VALUES (?, ?, ?, ?)', 
                     (t, a, p.get("price"), p.get("isbn")))
    db.commit()
    
    book = dict(db.execute('SELECT * FROM books WHERE id = ?', (cur.lastrowid,)).fetchone())
    resp = make_response(jsonify(book), 201)
    resp.headers["Location"] = f"/books/{book['id']}"
    return resp

# PUT /books/<id>: Cập nhật toàn bộ thông tin sách
@app.put("/books/<int:bid>")
def put(bid):
    p = request.get_json(silent=True) or {}
    t, a = p.get("title"), p.get("author")
    if not t or not a: return jsonify(error="need title+author"), 422

    db = get_db()
    cur = db.execute('UPDATE books SET title = ?, author = ?, price = ?, isbn = ? WHERE id = ?',
                     (t.strip(), a.strip(), p.get("price"), p.get("isbn"), bid))
    db.commit()
    if cur.rowcount == 0: return jsonify(error="not found"), 404
    
    book = dict(db.execute('SELECT * FROM books WHERE id = ?', (bid,)).fetchone())
    return jsonify(book), 200

# PATCH /books/<id>: Cập nhật một phần thông tin sách
@app.patch("/books/<int:bid>")
def patch(bid):
    p = request.get_json(silent=True) or {}
    if p.get("price", 0) < 0: return jsonify(error="price must be positive"), 422

    db = get_db()
    book = db.execute('SELECT * FROM books WHERE id = ?', (bid,)).fetchone()
    if book is None: return jsonify(error="not found"), 404

    fields, params = [], []
    for k in ["title", "author", "isbn", "price"]:
        if k in p:
            fields.append(f"{k} = ?")
            params.append(p[k])
    
    if fields:
        params.append(bid)
        db.execute(f'UPDATE books SET {", ".join(fields)} WHERE id = ?', params)
        db.commit()
        
    updated_book = dict(db.execute('SELECT * FROM books WHERE id = ?', (bid,)).fetchone())
    return jsonify(updated_book), 200

# DELETE /books/<id>: Xóa sách
@app.delete("/books/<int:bid>")
def delete(bid):
    db = get_db()
    cur = db.execute('DELETE FROM books WHERE id = ?', (bid,))
    db.commit()
    if cur.rowcount == 0: return jsonify(error="not found"), 404
    return "", 204

# GET /orders/: Lấy danh sách đơn hàng
@app.get("/orders/")
def list_orders():
    db = get_db()
    items = [dict(row) for row in db.execute('SELECT * FROM orders').fetchall()]
    return jsonify({"data": items, "total": len(items)}), 200

# GET /orders/<id>: Lấy chi tiết đơn hàng
@app.get("/orders/<int:oid>")
def fetch_order(oid):
    db = get_db()
    order = db.execute('SELECT * FROM orders WHERE id = ?', (oid,)).fetchone()
    if order is None: 
        return jsonify(error="order not found"), 404
    return jsonify(dict(order)), 200

# POST /orders/: Tạo mới đơn hàng
@app.post("/orders/")
def create_order():
    if not request.is_json: 
        return jsonify(error="expected JSON"), 415
        
    p = request.get_json(silent=True) or {}
    item = (p.get("item_name") or "").strip()
    qty = p.get("quantity")

    if not item or type(qty) is not int or qty <= 0: 
        return jsonify(error="valid item_name and positive quantity required"), 422

    db = get_db()
    cur = db.execute('INSERT INTO orders (item_name, quantity) VALUES (?, ?)', (item, qty))
    db.commit()
    
    order = dict(db.execute('SELECT * FROM orders WHERE id = ?', (cur.lastrowid,)).fetchone())
    resp = make_response(jsonify(order), 201)
    resp.headers["Location"] = f"/orders/{order['id']}"
    return resp

# PUT /orders/<id>: Cập nhật toàn bộ đơn hàng
@app.put("/orders/<int:oid>")
def put_order(oid):
    p = request.get_json(silent=True) or {}
    item = (p.get("item_name") or "").strip()
    qty = p.get("quantity")

    if not item or type(qty) is not int or qty <= 0:
        return jsonify(error="valid item_name and positive quantity required"), 422

    db = get_db()
    cur = db.execute('UPDATE orders SET item_name = ?, quantity = ? WHERE id = ?', 
                     (item, qty, oid))
    db.commit()
    
    if cur.rowcount == 0: 
        return jsonify(error="order not found"), 404
        
    order = dict(db.execute('SELECT * FROM orders WHERE id = ?', (oid,)).fetchone())
    return jsonify(order), 200

# PATCH /orders/<id>: Cập nhật một phần đơn hàng
@app.patch("/orders/<int:oid>")
def patch_order(oid):
    p = request.get_json(silent=True) or {}
    db = get_db()
    
    # Kiểm tra tồn tại
    order = db.execute('SELECT * FROM orders WHERE id = ?', (oid,)).fetchone()
    if order is None: 
        return jsonify(error="order not found"), 404

    fields, params = [], []
    
    if "item_name" in p:
        item = str(p["item_name"]).strip()
        if not item: return jsonify(error="item_name cannot be empty"), 422
        fields.append("item_name = ?")
        params.append(item)
        
    if "quantity" in p:
        qty = p["quantity"]
        if type(qty) is not int or qty <= 0: return jsonify(error="quantity must be positive int"), 422
        fields.append("quantity = ?")
        params.append(qty)

    if fields:
        params.append(oid)
        db.execute(f'UPDATE orders SET {", ".join(fields)} WHERE id = ?', params)
        db.commit()
        
    updated_order = dict(db.execute('SELECT * FROM orders WHERE id = ?', (oid,)).fetchone())
    return jsonify(updated_order), 200

# DELETE /orders/<id>: Xóa đơn hàng
@app.delete("/orders/<int:oid>")
def delete_order(oid):
    db = get_db()
    cur = db.execute('DELETE FROM orders WHERE id = ?', (oid,))
    db.commit()
    
    if cur.rowcount == 0: 
        return jsonify(error="order not found"), 404
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)