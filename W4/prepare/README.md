# Chuẩn bị nội dung Buổi 5: Data Modeling và Resource Design

## I. KIẾN THỨC NỀN TẢNG
---

### 1. Data Modeling và Resource Design là gì?

- **Data Modeling (Mô hình dữ liệu):** Là bước vạch ra trên giấy xem hệ thống có những thực thể nào (như học sinh, lớp học, môn học) và chúng liên kết với nhau ra sao.

- **Các kiểu quan hệ:**
    + Quan hệ 1-1: Một CMND chỉ thuộc về một người.
    + Quan hệ 1-n: Một lớp học có nhiều học sinh.
    + Quan hệ n-n: Một học sinh học nhiều môn học, và một môn học có nhiều học sinh.

- **Resource Design:** Từ mô hình dữ liệu trên, chuyển đổi chúng thành các đường dẫn (URL/Endpoint) trên Internet để các ứng dụng khác có thể gọi vào lấy dữ liệu. Quá trình chọn đường dẫn nào là gốc, đường dẫn nào lồng bên trong gọi là thiết kế cây tài nguyên (Resource Tree).

### 2. Chiến lược phân trang (Pagination)

Nếu trả về lượng lớn (ví dụ 10,000) bản ghi cùng lúc, ứng dụng sẽ treo. Phân trang giúp chỉ tải 10-20 bản ghi mỗi lần, giúp giảm tải hệ thống và tối ưu tương tác người dùng. 

- **3 kiểu phổ biến:**
    + **Page-based (Trang 1, 2, 3):** Gửi số trang lên (?page=2).
    + **Offset/Limit (Cắt theo độ dài):** Bỏ qua 20 mục đầu, lấy 10 mục tiếp theo (?offset=20&limit=10).
    + **Cursor (Đánh dấu mốc):** Lấy 10 mục tiếp theo kể từ bản ghi có mã số 100 (?cursor=100).

---

## II. THIẾT KẾ MÔ HÌNH QUẢN LÝ THƯ VIỆN
---

### 1. Mô hình quan hệ dữ liệu (Data Modeling)

Các thực thể (Entities) và Quan hệ (Relationships):

- **Book (Đầu sách - Thông tin chung):**
    + Thuộc tính: `id`, `isbn`, `title`, `description`, `published_year`.
    + Quan hệ: 1 đầu sách (Book) có nhiều bản sao vật lý (BookCopy) - (Quan hệ 1-N).

- **BookCopy (Bản sao sách vật lý - Cuốn sách cụ thể cầm trên tay):**
    + Thuộc tính: `id`, `book_id`, `barcode`, `condition`, `status (available, borrowed, lost)`.
    + Quan hệ: 1 bản sao chỉ thuộc về 1 đầu sách (N-1). Lượt mượn (Loan) sẽ gắn với bản sao này (1-1).

- **Author (Tác giả):**
    + Thuộc tính: `id`, `name`, `biography`.
    + Quan hệ: 1 Tác giả có nhiều Đầu sách, 1 Đầu sách có nhiều Tác giả - (Quan hệ N-N).

- **User (Người dùng):**
    + Thuộc tính: `id`, `member_code`, `name`, `email`, `status (active, suspended)`.
    + Quan hệ: 1 Độc giả có nhiều Lượt mượn (Loan) và nhiều Đặt trước (Reservation) - (Quan hệ 1-N).

- **Loan (Giao dịch mượn/trả):**
    + Thuộc tính: `id`, `user_id`, `book_copy_id`, `borrow_date`, `due_date`, `return_date`, `status (active, returned, overdue)`.
    + Quan hệ: Kết nối 1-1 với một BookCopy cụ thể trong một thời điểm, thuộc về 1 User.

- **Reservation (Yêu cầu đặt sách trước):**
    + Thuộc tính: `id`, `user_id`, `book_id`, `request_date`, `status (pending, fulfilled, cancelled)`.
    + Quan hệ: Kết nối User và Book (Đầu sách, vì độc giả đặt sách chung chứ không đặt mã vạch cụ thể).

### 2. Thiết kế Resource Tree (Cấu trúc URL)

Dựa trên mô hình quan hệ trên, API được thiết kế theo nguyên tắc: Top-level cho thực thể độc lập, Nested cho thực thể phụ thuộc chặt chẽ (1-N).

- **Top-level Resources (Dành cho truy vấn chung):**
    + `GET /books`: Danh sách đầu sách (Hỗ trợ query: ?authorId=123&sort=published_year).
    + `GET /books/{id}`: Xem chi tiết một đầu sách.
    + `GET /authors`: Danh sách tác giả.
    + `GET /users`: Danh sách độc giả (Dành cho thủ thư).

- **Nested Resources (Thể hiện sự phụ thuộc và tính sở hữu):**
    + `GET /books/{id}/copies`: Lấy danh sách các cuốn sách vật lý (mã vạch cụ thể) của một đầu sách. (Vì bản sao không thể tồn tại nếu không có đầu sách).
    + `POST /users/{id}/loans`: Thực hiện cho mượn một cuốn sách (gắn với độc giả).
    + `GET /users/{id}/loans`: Xem lịch sử mượn trả của riêng độc giả đó.
    + `GET /users/{id}/reservations`: Xem danh sách đặt trước của độc giả.

- **Resource giao dịch độc lập (Dành cho nghiệp vụ tổng hợp):**
    + `GET /loans`: Quản lý toàn bộ danh sách đang mượn/quá hạn của cả thư viện. (Hỗ trợ query: ?status=overdue).
    + `PATCH /loans/{id}`: Cập nhật trạng thái một lượt mượn (ví dụ: thực hiện thao tác Trả sách - đổi status thành 'returned').


### 3. SourceCodes

Giả lập API lấy danh sách sách có hỗ trợ lọc (theo id tác giả) và phân trang kiểu Offset.

[p_app](/W4/tasks-api/p_app.py)

### 4. Ảnh test

![W4_prepare_GET_book_OffsetPagi](https://github.com/user-attachments/assets/b82532a8-c1ae-4da9-b895-aaa02268d04d)

*Ảnh 1: Test GET_book_OffsetPagi*

![W4_prepare_GET_copies](https://github.com/user-attachments/assets/672dafe9-91c4-4420-a251-71f9ab7abbed)

*Ảnh 2: Test GET_BookCopies*

---

## III. 3 CÂU HỎI THỰC TẾ
---

### 1. Khi nào trả Task đầy đủ, khi nào trả TaskSummary?

- **Trả TaskSummary (Bản tóm tắt):** Sử dụng khi client gọi lấy danh sách (Collection) như `GET /tasks`. Việc trả về hàng trăm bản ghi mà mỗi bản ghi đều chứa dữ liệu cồng kềnh (như nội dung mô tả dài, file đính kèm) sẽ làm quá tải băng thông mạng và làm chậm server. Summary chỉ nên chứa các trường thiết yếu để hiển thị danh sách (id, title, status).

- **Trả Task đầy đủ:** Sử dụng khi client gọi lấy chi tiết một bản ghi cụ thể (Singleton) như `GET /tasks/{id}`. Lúc này client đã chọn một mục và cần toàn bộ thông tin chi tiết để hiển thị giao diện xem/chỉnh sửa.

### 2. Cursor vs Offset pagination — đánh đổi gì?

- **Offset Pagination (Dùng limit và offset):**
    + **Cách hoạt động:** Bỏ qua N bản ghi đầu tiên và lấy X bản ghi tiếp theo (Giống như nhảy tới trang 5).
    + **Ưu điểm:** Dễ hiểu, dễ code, cho phép người dùng nhảy cóc đến một trang bất kỳ.
    + **Nhược điểm (Đánh đổi):** 
        + Hiệu năng cực kỳ tệ khi bảng dữ liệu lớn (truy vấn OFFSET 1000000 sẽ buộc database phải duyệt qua 1 triệu bản ghi trước khi lấy dữ liệu). 
        + Gặp lỗi "lệch dữ liệu": Nếu đang ở trang 1, có ai đó thêm bản ghi mới lên đầu danh sách, khi sang trang 2 bạn sẽ bị nhìn thấy lại bản ghi cũ của trang 1.

- **Cursor Pagination (Dùng con trỏ):**
    + **Cách hoạt động:** Sử dụng ID hoặc Timestamp của bản ghi cuối cùng ở trang trước làm mốc (Ví dụ: Lấy 10 sách có ID > 15).
    + **Ưu điểm:** Tốc độ truy vấn cực nhanh bất kể dữ liệu lớn. Tránh được hoàn toàn lỗi lệch/trùng dữ liệu khi có bản ghi mới chèn vào.
    + **Nhược điểm (Đánh đổi):** Không thể nhảy cóc trang (Không thể từ trang 1 bấm sang thẳng trang 10). Khó code hơn đối với các tính năng sắp xếp phức tạp. Phù hợp cho tính năng "Cuộn vô tận" (Infinite scroll).

### 3. Nested resource (/users/{id}/tasks) vs query (/tasks?userId={id}) — khi nào cái nào tốt hơn?

Theo James Higginbotham, nên giữ URL càng phẳng (shallow) càng tốt. Việc lồng ghép (nesting) quá sâu (ví dụ /a/1/b/2/c/3) là tối kỵ.

- Dùng `Nested Resource (/users/{id}/tasks)`:
Nên dùng khi dữ liệu có tính sở hữu tuyệt đối và sự phụ thuộc chặt chẽ (Aggregation).

Ví dụ: Task này thuộc về riêng User này, nếu User bị xoá thì Task cũng biến mất. Việc đặt trong /users/{id} thể hiện rõ ràng ngữ cảnh: "Tôi đang xem các công việc **CỦA** tài khoản này".

- Dùng `Query (/tasks?userId={id})`:
Nên dùng khi resource là một thực thể độc lập cấp cao (Top-level resource) và cần cung cấp khả năng tìm kiếm chéo nhiều tiêu chí.

Ví dụ: Một hệ thống có bộ lọc phức tạp. Dùng Query cho phép bạn kết hợp linh hoạt: `/tasks?userId=123&status=open&priority=high`. Nếu dùng Nested, việc thiết kế URL để lọc qua lại giữa nhiều tiêu chí sẽ bế tắc.

---