# Chuẩn bị nội dung Buổi 4: API Specification và OpenAPI

## 1. Định nghĩa
---

- **OpenAPI Specification (OAS):** Là một định dạng chuẩn độc lập với ngôn ngữ lập trình (thường viết bằng YAML hoặc JSON) dùng để mô tả chi tiết các endpoint, tham số, xác thực và cấu trúc dữ liệu trả về của một RESTful API.

- **Swagger UI:** Là công cụ đọc file OpenAPI (YAML/JSON) và tự động tạo ra một giao diện web trực quan, cho phép con người đọc tài liệu và tương tác gửi request thử nghiệm trực tiếp trên trình duyệt.

---

## 2. Cấu trúc file OpenAPI cơ bản
---

Một file `openapi.yaml` đạt chuẩn chứa 4 khối thành phần chính:

- `openapi`: Khai báo phiên bản (ví dụ: 3.0.0).
- `info`: Chứa metadata như `title`, `version`, `description`.
- `paths`: Định nghĩa toàn bộ các URL endpoints (ví dụ: `/books`) và các `HTTP methods (get, post, put, delete)` tương ứng.
- `components`: Nơi tái sử dụng các cấu trúc dữ liệu. Bao gồm:
    - `schemas`: Định nghĩa cấu trúc model (ví dụ: đối tượng Book gồm id, title).
    - `parameters`: Định nghĩa các tham số dùng chung (ví dụ: path parameter {id}).
    - `securitySchemes`: Cấu hình xác thực (ví dụ: Bearer Token).

---

## Liên hệ JJ Geewax - Chương 2

---

Theo JJ Geewax trong Chương 2 (Resource-Oriented APIs), một API chuẩn mực phải xoay quanh các tài nguyên (Resources) thay vì hành động.
Việc sử dụng OpenAPI ép buộc lập trình viên phải tư duy theo hướng này thông qua việc định nghĩa `paths` dựa trên danh từ (tài nguyên) và gán các `methods` tiêu chuẩn cho chúng.
Geewax đưa ra 5 method tiêu chuẩn (Standard Methods) để thao tác với tài nguyên: `List, Get, Create, Update, Delete`. Cấu trúc 4 phần của OpenAPI giúp chuẩn hóa 5 hành động này, tách biệt rõ ràng phần định tuyến (`paths`) và phần định nghĩa dữ liệu (`components/schemas`), giúp giảm thiểu trùng lặp code khi tài liệu hóa.

---

## 3. Thực hành thiết kế API Quản lý sách (5 Endpoints)

---

### 3.1. File cấu hình openapi.yaml

[openapi](/W3/api_design/openapi.yaml)

### 3.2 Flask (Tích hợp Swagger UI)

[app](/W3/api_design/app.py)

### 3.3. Kiểm thử

- List Books:

![W3_prepare_GET_list](https://github.com/user-attachments/assets/32f4f062-d7df-44d7-a85e-ef7ae7051543)
*Hình 1: Test Get List Books*

- Create Book:

![W3_prepare_POST](https://github.com/user-attachments/assets/5858b36c-5c79-4f28-9b47-6d91fd27da27)
*Hình 2: Test Create Book (POST)*

- Get Book:

![W3_prepare_GET_id](https://github.com/user-attachments/assets/e7e4d0f5-db58-4612-aa19-9bf81fb57980)
*Hình 3: Test Get Book (GET ID=2)*

- Update Book:

![W3_prepare_PUT](https://github.com/user-attachments/assets/94ea9839-06fb-4029-9d6a-89acd76e5c96)
*Hình 4: Test Update Book (PUT ID=2)*

- Delete Book:

![W3_prepare_DELETE](https://github.com/user-attachments/assets/971f67c2-bc9e-448e-9dd3-f96e087ac239)
*Hình 5: Test Delete Book (DELETE ID=2)*

---