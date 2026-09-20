# Chuẩn bị nội dung Buổi 3: Nguyên tắc Thiết kế API

## 1. Các best practices (Quy tắc thiết kế)
---

### 1.1. Tính nhất quán (consistency)
- Áp dụng chung một cấu trúc JSON trả về và một quy chuẩn URL cho toàn bộ dự án.

### 1.2. Tính dễ hiểu/rõ ràng (clarity)
- URL chỉ chứa `tài nguyên (resource)`, không chứa `động từ hành động (action verbs)`. Động từ được xác định bởi `HTTP Methods (GET, POST, PUT, DELETE)`.

### 1.3. Tính dễ mở rộng (extensibility)
- Hỗ trợ `query parameters` cho việc lọc, phân trang thay vì tạo endpoint mới (VD: `/v1/books?author=Orwell`).

**(?)** Một API tốt không bắt client phải đoán. Nếu tạo sách là `POST /books`, thì tạo đơn hàng phải là `POST /orders`, không thiết kế thành `POST /createNewOrder`. 

---

## 2. Naming conventions (Cách đặt tên)
---

### 2.1. Plural nouns (Danh từ số nhiều)
- Dùng `/users`, `/books` (Không dùng danh từ số ít `/user`, `/book`).
- **(?)** Theo James Higginbotham, một endpoint đại diện cho một `tập hợp (collection)` các tài nguyên.
### 2.2. Lowercase (Chữ thường)
- Dùng `/users`, `/books` (Không dùng chữ hoa `/Users`, `/Books`).
- **(?)** URL có phân biệt chữ hoa chữ thường trên một số hệ điều hành (như Linux). Dùng toàn bộ chữ thường giúp tránh lỗi `typo 404 Not Found`.
### 2.3. Hyphens (Gạch ngang)
- Dùng kebab-case `/book-categories` (Không dùng gạch dưới snake_case `/book_categories` hay viết liền camelCase `/bookCategories`).
- **(?)** Dấu gạch ngang (kebab-case) được các công cụ tìm kiếm và trình duyệt đọc hiểu dễ dàng hơn dấu gạch dưới.
### 2.4. Versioning
- **Bắt buộc** có phiên bản ở URL, ví dụ: `/v1/books`.
- **(?)** Việc gắn `/v1/` đảm bảo khi nghiệp vụ thay đổi ở bản `/v2/`, các ứng dụng cũ dùng `/v1/` không bị sập.

---

## 3. Case Study: Một số ví dụ lỗi trong một API poorly designed
---

- **(A)** `GET /getAllBooks`
-> `GET /v1/books`

- **(B)** `POST /orders/createNew`
-> `POST /v1/orders`

- **(C)** `GET /Book/1`
-> `GET /v1/books/1`

- **(D)** `POST /books/1/update`
-> `PUT /v1/books/1` hoặc `PATCH /v1/books/1`

- Giải thích lỗi:
    + **(A) và (B) lỗi Clarity:** URL chứa `động từ`
    + **(C) lỗi Plural nouns và Lowercase:** Danh từ số ít và viết hoa
    + **(D) lỗi Clarity và định nghĩa HTTP method:** dùng động từ `update` cùng method `POST` để cập nhật thay vì `PUT/PATCH`

---

## 4. Tự đánh giá thiết kế API hiện tại của bản thân
--- 

- Theo đánh giá sơ bộ: Các bản thực hành đơn giản [W2/app.py](/W2/api_session_02/app.py) hay [W2/h_app.py](/W2/api_session_02/h_app.py) hiện tại còn thiếu tính `Versioning`, nếu muốn sửa tính năng, hiện tại cần sửa HTTP method gốc hoặc cần bổ sung phiên bản cho các HTTP method để tránh xung đột. 
- Ví dụ:
```bash
# Lấy sách theo id
@app.get("/books/<int:bid>")
```
-> Sửa thành:
```bash
# Lấy sách theo id (phiên bản v1)
@app.get("v1/books/<int:bid>")
```
