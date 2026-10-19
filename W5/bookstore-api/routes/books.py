from flask import Blueprint, request, jsonify
from jsonschema import validate, ValidationError
from sqlalchemy import select, func, tuple_
import json
import os
import base64
from models import db, Book

bp = Blueprint('books', __name__, url_prefix='/api/v1/books')

# Load schema
schema_path = os.path.join(os.path.dirname(__file__), '../schemas/book.json')
with open(schema_path) as f:
    SCHEMA = json.load(f)

# --- PHÂN TRANG CURSOR ---
# Whitelist chống SQL Injection khi sort
SORT_WHITELIST = {"id": Book.id, "price": Book.price_amount, "title": Book.title}

def parse_multi_sort(raw_sort):
    cols = []
    keys = raw_sort.split(",")
    primary_key = None
    desc = False
    
    for idx, key in enumerate(keys):
        is_desc = key.startswith("-")
        name = key.lstrip("-")
        
        if name not in SORT_WHITELIST:
            return None, None, False, f"bad_sort_key: {name}"
            
        p_col = SORT_WHITELIST[name]
        cols.append(p_col.desc() if is_desc else p_col.asc())
        
        # Lưu lại key đầu tiên để làm Cursor
        if idx == 0:
            primary_key = p_col
            desc = is_desc
            
    # Luôn thêm ID làm tie-breaker để tránh trùng lặp
    cols.append(Book.id.desc() if desc else Book.id.asc())
    return primary_key, cols, desc, None

# --- ROUTES ---
@bp.get("")
def list_books():
    strategy = request.args.get("strategy", "cursor")
    lim = min(request.args.get("limit", 20, type=int), 100)
    genre = request.args.get("genre")
    sort_raw = request.args.get("sort", "-id")
    
    # Áp dụng Filter genre
    q = select(Book)
    if genre:
        # Giả định Book model đã có cột genre
        q = q.filter(Book.genre == genre)

    # Xử lý Multi-key Sort
    primary_col, sort_cols, is_desc, err = parse_multi_sort(sort_raw)
    if err:
        return jsonify({"error": err}), 400
    q = q.order_by(*sort_cols)

    # Phân trang Offset
    if strategy == "offset":
        offset = request.args.get("offset", 0, type=int)
        total = db.session.scalar(select(func.count(Book.id)))
        rows = db.session.scalars(q.offset(offset).limit(lim)).all()
        
        return jsonify({
            "data": [b.to_dict() for b in rows],
            "pagination": {
                "offset": offset, 
                "limit": lim, 
                "total": total,
                "has_next": (offset + lim) < total
            }
        }), 200

    # Phân trang Cursor
    raw_cursor = request.args.get("cursor")
    if raw_cursor:
        pad = "=" * (-len(raw_cursor) % 4)
        try:
            c = json.loads(base64.urlsafe_b64decode(raw_cursor + pad))
            # Chỉ validate cursor bằng primary sort key
            if c.get("s") != sort_raw.split(",")[0]:
                return jsonify({"error": "sort_changed_invalid_cursor"}), 400
                
            v, i = c["v"], c["i"]
            op = "<" if is_desc else ">"
            condition = tuple_(primary_col, Book.id).op(op)((v, i))
            q = q.filter(condition)
        except Exception:
            return jsonify({"error": "malformed_cursor"}), 400

    rows = db.session.scalars(q.limit(lim + 1)).all()
    has_more = len(rows) > lim
    items = rows[:lim]
    
    nxt = None
    if items and has_more:
        last = items[-1]
        sort_val = getattr(last, primary_col.name) if primary_col.name != "price_amount" else last.price_amount
        nxt_dict = {"s": sort_raw.split(",")[0], "v": sort_val, "i": last.id}
        nxt = base64.urlsafe_b64encode(json.dumps(nxt_dict).encode()).decode().rstrip("=")

    return jsonify({
        "data": [b.to_dict() for b in items],
        "pagination": {"next_cursor": nxt, "has_more": has_more}
    }), 200

@bp.get("/<int:book_id>")
def get_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"error": "not_found", "message": "Book not found"}), 404
    return jsonify(book.to_dict()), 200

@bp.post("")
def create_book():
    payload = request.get_json(silent=True) or {}
    
    try:
        validate(payload, SCHEMA)
    except ValidationError as e:
        return jsonify({
            "error": "validation_failed",
            "field": list(e.path),
            "message": e.message
        }), 400

    book = Book(
        title=payload['title'],
        isbn=payload.get('isbn'),
        genre=payload.get('genre'),
        category_id=payload.get('category_id'),
        price_amount=payload['price']['amount'],
        price_currency=payload['price']['currency']
    )
    db.session.add(book)
    db.session.commit()
    
    return jsonify(book.to_dict()), 201

@bp.put("/<int:book_id>")
def update_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"error": "not_found", "message": "Book not found"}), 404
        
    payload = request.get_json(silent=True) or {}
    
    try:
        validate(payload, SCHEMA)
    except ValidationError as e:
        return jsonify({
            "error": "validation_failed",
            "field": list(e.path),
            "message": e.message
        }), 400

    book.title = payload['title']
    book.isbn = payload.get('isbn')
    book.genre = payload.get('genre')
    book.category_id = payload.get('category_id')
    book.price_amount = payload['price']['amount']
    book.price_currency = payload['price']['currency']
    
    db.session.commit()
    return jsonify(book.to_dict()), 200

@bp.delete("/<int:book_id>")
def delete_book(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"error": "not_found", "message": "Book not found"}), 404
        
    db.session.delete(book)
    db.session.commit()
    return '', 204