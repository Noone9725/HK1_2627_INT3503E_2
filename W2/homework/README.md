# Homework W2

## File code B1 + B3: 
[h_app](/W2/api_session_02/h_app.py)

## Dump database:
[data.db](/W2/api_session_02/data.db)
[data.sql](/W2/api_session_02/backup.sql)

## Bài 1: Refactor /orders sang SQLite
---
- `get_db()` với `g của Flask`: quản lý kết nối database trên mỗi request.
- `init_db()` để tự tạo bảng `books`, bảng `orders`, chèn dữ liệu mẫu nếu bảng trống trong lần chạy đầu tiên.
- Các `endpoint (GET, POST, PUT, PATCH, DELETE)` để thực thi SQL code thay vì thao tác list Python.
- Endpoint `GET /orders/` thực thi truy vấn trên bảng `orders`.

- **Chạy:**
```bash
# Khởi tạo API + Tự tạo database khởi đầu data.db
python h_app.py 
```

```bash
# Chuyển data.db thành backup.sql
python dump_db.py
```
---
## Bài 2: Audit một public API thực (GitHub REST API)
---
| Endpoint | Method | Status Code | Headers bắt buộc / Quan trọng | RESTful? |
|---|---|---|---|---|
| `/users/{username}` | GET | 200 OK | `Accept: application/vnd.github+json`<br>`Authorization: Bearer <token>` | Có |
| `/user/repos` | POST | 201 Created | `Accept: application/vnd.github+json`<br>`Authorization: Bearer <token>` | Có |
| `/repos/{owner}/{repo}` | PATCH | 200 OK | `Accept: application/vnd.github+json`<br>`Authorization: Bearer <token>` | Có |
| `/repos/{owner}/{repo}` | DELETE | 204 No Content | `Accept: application/vnd.github+json`<br>`Authorization: Bearer <token>` | Có |
| `/repos/{owner}/{repo}/subscription` | PUT | 200 OK | `Accept: application/vnd.github+json`<br>`Authorization: Bearer <token>` | Có |

- **Headers:** metadata gửi kèm request, GitHub yêu cầu `Accept` để versioning `Authorization` để xác thực người dùng.
- **RESTful?:** 
    + Dùng danh từ để chỉ tài nguyên (`/users, /repos`)
    + Dùng HTTP Method để định nghĩa hành động.
    + Cấu trúc định tuyến cấp bậc (`/repos/{owner}/{repo}`)

--- 

## Bài 3: Conditional requests với ETag
---
- **Đoạn thực hiện:** (Phần `GET /books`, Dòng `117-131`)
```bash
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
```

- **Hoạt động:**
    + Khi client gọi `GET /books/` , server trả về danh sách sách kèm 1 mã định danh ETag.
    + Lần gọi sau, client gửi kèm ETag này lên server qua header `If-None-Match`.
    + Server so với mã sinh ra từ dữ liệu hiện tại, nếu khớp -> không có sách nào thay đổi, không cần gửi lại phần lớn data, chỉ báo mã 304.

## Ảnh Test:
![W2_H_GET_list_200](https://github.com/user-attachments/assets/d4197fc7-49d8-414d-b90a-4af40781c57c)
*Hình 1: Test W2_H_GET_listbooks_200_OK from SQLite*

![W2_H_Orders]https://github.com/user-attachments/assets/eb0deade-8e7b-40cc-a86b-09f793fb7c2d)
*Hình 2: Test POST&GET_Orders form SQLite*

![W2_H_ETag_304](https://github.com/user-attachments/assets/3b0f6d5d-00f7-44a1-b62d-74b7b6a7137a)
*Hình 3: Test ETag_304_NOT_MODIFIED B3*

![W2_H_ETag_200](https://github.com/user-attachments/assets/ef378f6d-18e8-4e6d-998e-53da8d73353f)
*Hình 4: Test ETag_MODIFIED_200_OK(GET) B3*
---