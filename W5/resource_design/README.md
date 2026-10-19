# Resource Design for Library Domain

## I. ERD

![ERD](https://github.com/user-attachments/assets/da63c443-e5d8-4bb6-8f5c-ee5d57e970d4)

*Hình 1: ERD của Library Domain (Basic)*

## II. Resource & URL Endpoints List

### 1. Sách (Books)

- `GET /books`: Lấy danh sách sách. Hỗ trợ query parameters để filter: `?author`, ?`category`, `?in_stock`

- `GET /books/{id}`: Lấy chi tiết 1 cuốn sách (nhúng sẵn thông tin tác giả, thể loại, số lượng tồn kho).

- `POST /books`: Thêm sách mới (Admin).

- `PUT /books/{id}`: Cập nhật thông tin sách (Admin)..

- `DELETE /books/{id}`: Xóa sách (Admin).

- `GET /books/{id}/loans`: Lấy danh sách các lượt mượn của cuốn sách này, bao gồm thông tin ai đã mượn và tình trạng (Admin).

### 2. Tác giả (Authors)

- `GET /authors`: Lấy danh sách tác giả.

- `GET /authors/{id}`: Lấy thông tin chi tiết của 1 tác giả.

- `GET /authors/{id}/books`: Lấy danh sách sách (dạng tóm tắt) do tác giả này viết.

### 3. Thành viên (Members)

-  `GET /members`: Lấy danh sách thành viên (Admin).

-  `POST /members`: Đăng ký thành viên mới.

-  `GET /members/{id}`: Lấy thông tin cá nhân.

- `DELETE /members/{id}`: Xóa tài khoản (Có thể là vô hiệu hóa/Soft-delete nếu vướng lịch sử mượn).

- `PUT /members/{id}`: Cập nhật thông tin thành viên.

- `GET /members/{id}/loans`: Lấy lịch sử mượn/trả sách của chính bản thân (bao gồm sách gì, hạn trả, tình trạng).

### 4. Lượt mượn trả (Loans - Giao dịch)

- `POST /loans`: Tạo mới 1 lượt mượn sách (Hệ thống tự động trừ `stock` của sách).

- `GET /loans`: Lấy danh sách mượn sách toàn hệ thống (Admin).

- `GET /loans/{id}`: Lấy chi tiết 1 phiếu mượn.

- `PATCH /loans/{id}`: Cập nhật trạng thái phiếu mượn (ví dụ: trả sách, quá hạn, hệ thống tự động cộng lại `stock` cho sách sau khi nhận trạng thái trả).

### 5. Danh mục (Categories)

- `GET /categories`: Lấy danh sách thể loại sách.

- `GET /categories/{id}`: Lấy thông tin chi tiết của 1 thể loại.

- `GET /categories/{id}/books`: Lấy danh sách sách (dạng tóm tắt) thuộc thể loại này.

## III. JSON Schema cho 3 Resource chính

1. Book (Sách)

- Bản Input cho `POST / PUT`:

[Book Input](/W5/resource_design/schemas/book_input.json)

- Bản cho `GET /books/{id}`:

[Book Detail](/W5/resource_design/schemas/book_detail.json)


- Bản cho `GET /books`, `GET /categories/{id}/books`, `GET /authors/{id}/books`:

[Book Summary](/W5/resource_design/schemas/book_summary.json)

2. Member (Thành viên)

[Member](/W5/resource_design/schemas/member.json)

3. Loan (Phiếu mượn)

[Loan](/W5/resource_design/schemas/loan.json)

