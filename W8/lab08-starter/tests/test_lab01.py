"""LAB 1 — add your five tests here. Do not delete the smoke tests.

A. GET /books, empty database -> HTTP 200 and []
B. GET /books/9999 -> HTTP 404, JSON code == NOT_FOUND
C. POST /books with only author -> HTTP 400, errors contains title
D. POST valid book, DELETE it, GET same id -> HTTP 404
BONUS. Validate a Book response using JSON Schema; add an unknown
       field to a *copy* of the response and assert ValidationError.

Useful imports:
    from jsonschema import validate, ValidationError
    import pytest
    from tools import get_book_schema

Do not depend on test execution order. Fixtures: client, create_app, sample_book.
"""

import pytest
from jsonschema import ValidationError, validate
from tools import get_book_schema


def test_get_books_empty_db(client):
    response = client.get("/books")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data == []


def test_get_book_not_found(client):
    response = client.get("/books/9999")
    data = response.get_json()

    assert response.status_code == 404
    assert data is not None
    assert data.get("code") == "NOT_FOUND"


def test_post_book_missing_title(client):
    payload_missing_title = {
        "author": "Một Tác Giả",
    }
    response = client.post("/books", json=payload_missing_title)
    data = response.get_json()

    assert response.status_code == 400
    assert "errors" in data
    assert any(err.get("field") == "title" for err in data["errors"])


def test_delete_then_get(client):
    # Tạo một bản ghi hợp lệ để lấy ID
    post_response = client.post(
        "/books",
        json={
            "title": "Book_test",
            "author": "Author_test",
        },
    )
    assert post_response.status_code == 201
    book_id = post_response.get_json()["id"]

    # Xoá bản ghi vừa tạo
    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 204

    # GET lại cùng ID sau khi xoá
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404
    assert get_response.get_json().get("code") == "NOT_FOUND"


def test_response_extra_field_blocked(client, sample_book):
    schema = get_book_schema()
    # Điều chỉnh type tương thích jsonschema với dữ liệu integer/null của Book
    schema["properties"]["year"]["type"] = ["integer", "null"]
    schema["properties"]["isbn"]["type"] = ["string", "null"]

    # Lấy dữ liệu sách mẫu từ backend
    response = client.get(f"/books/{sample_book}")
    assert response.status_code == 200
    data = response.get_json()

    # Validate response gốc phải hợp lệ theo JSON Schema
    validate(instance=data, schema=schema)

    # Giả lập thêm field lạ (password_hash) vào bản sao của response
    tampered_data = dict(data)
    tampered_data["password_hash"] = "pbkdf2:sha256:fake_password_hash"

    # Assert schema chặn trường lạ do additionalProperties: false
    with pytest.raises(ValidationError):
        validate(instance=tampered_data, schema=schema)