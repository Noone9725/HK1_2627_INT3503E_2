from flask import Flask, request, jsonify, make_response
from flasgger import Swagger

app = Flask(__name__)

# Cấu hình Swagger tự động render giao diện từ file openapi.yaml
app.config['SWAGGER'] = {
    'title': 'Book Management API',
    'uiversion': 3,
    'openapi': '3.0.0'
}
swagger = Swagger(app, template_file='openapi.yaml')

# Dữ liệu giả lập
books_db = [{"id": 1, "title": "API Design Patterns", "author": "JJ Geewax"}]

@app.route('/api/v1/books', methods=['GET'])
def list_books():
    return jsonify(books_db), 200

@app.route('/api/v1/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = {"id": len(books_db) + 1, "title": data['title'], "author": data.get('author', '')}
    books_db.append(new_book)
    return jsonify(new_book), 201

@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books_db if b['id'] == book_id), None)
    if not book:
        return jsonify({"error": "Not found"}), 404
    return jsonify(book), 200

@app.route('/api/v1/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((b for b in books_db if b['id'] == book_id), None)
    if not book:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    book['title'] = data.get('title', book['title'])
    book['author'] = data.get('author', book['author'])
    return jsonify(book), 200

@app.route('/api/v1/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books_db
    books_db = [b for b in books_db if b['id'] != book_id]
    return '', 204

if __name__ == '__main__':
    # Render Swagger UI tại: http://127.0.0.1:5000/apidocs/
    app.run(debug=True, port=5000)