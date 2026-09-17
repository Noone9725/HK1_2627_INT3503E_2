# B1 + B2 + B3 
from flask import Flask, jsonify, request, make_response
app = Flask(__name__)

# tham so phan trang
DEFAULT_SIZE, MAX_SIZE = 20, 100

# dataset mau mang sach, co id, title, author, price
BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "R. Martin", "price": 25.5},
    {"id": 2, "title": "Clean Architecture", "author": "R. Martin", "price": 28.0},
    {"id": 3, "title": "1984", "author": "Orwell", "price": 15.0},
    {"id": 4, "title": "Animal Farm", "author": "Orwell", "price": 12.0},
    {"id": 5, "title": "The Clean Coder", "author": "R. Martin", "price": 22.0},
    {"id": 6, "title": "Homage to Catalonia", "author": "Orwell", "price": 18.0},
    {"id": 7, "title": "Design Patterns", "author": "Erich Gamma", "price": 35.0},
    {"id": 8, "title": "Refactoring", "author": "Martin Fowler", "price": 40.0},
    {"id": 9, "title": "Pragmatic Programmer", "author": "Andrew Hunt", "price": 32.0},
    {"id": 10, "title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "price": 60.0},
    {"id": 11, "title": "Code Complete", "author": "Steve McConnell", "price": 45.0},
    {"id": 12, "title": "Mythical Man-Month", "author": "Frederick P. Brooks", "price": 20.0},
    {"id": 13, "title": "Clean Agile", "author": "R. Martin", "price": 24.0},
    {"id": 14, "title": "Burmese Days", "author": "Orwell", "price": 14.0},
    {"id": 15, "title": "Head First Design", "author": "Eric Freeman", "price": 38.0}
]
_next_id = 16

# # GET /books: tra danh sach
# @app.get("/books")
# def list_books():
#     return jsonify(
#         {
#             "data": BOOKS,
#             "total": len(BOOKS)
#         }
#     ), 200

# GET /books/<id>: lay sach theo id, cache 60s
@app.get("/books/<int:bid>")
def fetch(bid):
    i = next((k for k,b in enumerate(BOOKS) if b["id"]==bid), None)
    if i is None: return jsonify(error="not found"), 404

    resp = make_response(jsonify(BOOKS[i]), 200)
    resp.headers["Cache-Control"]="max-age=60"; 
    return resp

# GET /books: list + filter + paginate + links
@app.get("/books")
def list_books():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify(error="page and size must be int"), 400
    page = max(page, 1) 
    size = max(min(size, MAX_SIZE), 1)

    # filter: author chính xác, q tìm trong title
    flt = BOOKS
    a = request.args.get("author")
    if a: flt = [b for b in flt if b["author"].lower()==a.lower()]
    q = (request.args.get("q") or "").lower()
    if q: flt = [b for b in flt if q in b["title"].lower()]

    # paginate
    total = len(flt)
    start = (page-1) * size 
    end = start + size
    items = flt[start:end] 
    last = (total + size - 1) // size

    # HATEOAS links
    def u(p): 
        return f"/books?page={p}&size={size}"
    links = {
        "self":{"href":u(page)},
        "first":{"href":u(1)},
        "last":{"href":u(max(last,1))}
    }

    if page > 1: links["prev"] = {"href":u(page-1)}
    if end < total: links["next"]={"href":u(page+1)}

    body = {
        "data":items,
        "pagination":{"page":page,"size":size,"total":total,"total_pages":last},
        "_links":links
    }

    resp = make_response(jsonify(body), 200)
    resp.headers["Cache-Control"]="public, max-age=30"
    return resp

# POST /books: tao moi
@app.post("/books")
def create_book():
    global _next_id

    if not request.is_json:
        return jsonify(error="expected JSON"), 415

    p = request.get_json(silent=True) or {}
    t = (p.get("title") or "").strip()
    a = (p.get("author") or "").strip()
    if not t or not a:
        return jsonify(error="title and author required"), 422

    book = {"id": _next_id, "title": t, "author": a}

    BOOKS.append(book)
    _next_id += 1    
    resp = make_response(jsonify(book), 201)
    resp.headers["Location"] = f"/books/{book['id']}"
    return resp

# PUT /books/<id>: cap nhat toan bo, title+author bat buoc
@app.put("/books/<int:bid>")
def put(bid):
    i = next((k for k,b in enumerate(BOOKS) if b["id"]==bid), None)
    if i is None: return jsonify(error="not found"), 404

    p = request.get_json(silent=True) or {}
    t,a = p.get("title"), p.get("author")
    if not t or not a: return jsonify(error="need title+author"), 422

    BOOKS[i]={"id":bid,"title":t.strip(),"author":a.strip(),
    "isbn":p.get("isbn"),"price":p.get("price")}
    return jsonify(BOOKS[i]), 200

# PATCH /books/<id>: chi cap nhat field co trong body
@app.patch("/books/<int:bid>")
def patch(bid):
    i = next((k for k,b in enumerate(BOOKS) if b["id"]==bid), None)
    if i is None: return jsonify(error="not found"), 404

    p = request.get_json(silent=True) or {}
    if p.get("price", 0) < 0:
        return jsonify(error="price must be positive"), 422

    for k in "title author isbn price".split():
        if k in p: BOOKS[i][k] = p[k]
    return jsonify(BOOKS[i]), 200

# DELETE /books/<id>: idempotent, trả 204
@app.delete("/books/<int:bid>")
def delete(bid):
    i = next((k for k,b in enumerate(BOOKS) if b["id"]==bid), None)
    if i is None: return jsonify(error="not found"), 404
    BOOKS.pop(i)
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)