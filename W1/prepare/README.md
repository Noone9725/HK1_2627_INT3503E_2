## I. Câu hỏi cho buổi 2

### PUT vs PATCH khác nhau thế nào?
- **PUT:** Cập nhật toàn bộ/ghi đè tài nguyên (Replace).
- **PATCH:** Cập nhật một phần tài nguyên (Partial update).

**Ví dụ**: 
Giả sử resource sách là {"id": 1, "title": "A", "year": 2020}.
- Nếu client gửi `PUT {"year": 2021}`, resource mới sẽ thành `{"id": 1, "year": 2021}` (trường title bị xóa mất do cơ chế ghi đè toàn bộ).
- Nếu client gửi `PATCH {"year": 2021}`, resource mới sẽ thành `{"id": 1, "title": "A", "year": 2021}` (chỉ trường year bị thay đổi).
### "Khi nào 404 khác 410 Gone?"
- **404 Not Found:** Không tìm thấy dữ liệu ở thời điểm hiện tại (không rõ nguyên nhân hoặc tương lai có tồn tại lại hay không).
- **410 Gone:** Dữ liệu chắc chắn đã bị xóa vĩnh viễn, không bao giờ quay lại.

- 410 Gone được sử dụng để báo hiệu cho các công cụ (như Google Bot) hoặc client xóa lưu trữ cache và ngừng truy cập URL này vĩnh viễn, tiết kiệm tài nguyên mạng hơn so với việc liên tục crawl lại một URL báo lỗi 404.
### "Có bao nhiêu cache-control directive?"
- Có hơn `10 directives chuẩn`. 
- `6 directives cốt lõi nhất`: max-age, no-cache, no-store, public, private, must-revalidate.
- Cache-Control Directives:
    + `no-store`: Cấm mọi hình thức lưu cache (dùng cho dữ liệu cực kỳ nhạy cảm như OTP, mật khẩu).
    + `no-cache`: Client vẫn lưu cache, nhưng mỗi lần dùng phải gửi một request mồi lên server để hỏi xem cache còn hợp lệ không.
    + `max-age=3600`: Cache có giá trị sử dụng trong 3600 giây.

## II. 6 nguyên tắc REST chi tiết

### 1. Client-Server: Tách biệt giao diện và dữ liệu.
- `Client-Server`: `Backend (Server)` và `Frontend/Mobile (Client)` không liên quan đến công nghệ của nhau. 
- Backend không quan tâm client render màn hình thế nào, client không cần biết database backend dùng gì.
### 2. Stateless: Phi trạng thái.
- Server không lưu giữ bất kỳ thông tin session nào của client sau khi request kết thúc. 
- Mỗi request từ client gửi lên phải chứa toàn bộ thông tin cần thiết (như Token xác thực) để server hiểu.
### 3. Cacheable: Có khả năng lưu bộ nhớ đệm.
- Server phải dán nhãn cho response (thông qua headers) để báo cho client hoặc các proxy biết dữ liệu này có được phép lưu lại dùng cho các lần sau hay không.
### 4. Uniform Interface: Giao diện đồng nhất.
- Tất cả các API trong hệ thống phải tuân theo một quy tắc chung về định dạng URL, cách dùng HTTP methods và định dạng dữ liệu trả về (cùng là JSON).
### 5. Layered System: Hệ thống phân lớp.
- Client không thể biết được nó đang kết nối trực tiếp với server ứng dụng hay qua các máy chủ trung gian (Load balancer, Firewall, CDN).
### 6. Code-On-Demand (Tùy chọn): Trả về mã thực thi.
- Server có thể trả về một đoạn mã (như JavaScript) để client trực tiếp thực thi (ít dùng trong API dữ liệu hiện đại).

## III. HTTP Methods
- `GET`: Đọc dữ liệu (Read).
- `POST`: Tạo dữ liệu mới (Create).
- `PUT`: Ghi đè/Cập nhật toàn bộ (Update).
- `PATCH`: Cập nhật một phần (Partial Update).
- `DELETE`: Xóa (Delete).

- `Tính lũy đẳng (Idempotency)`: Một HTTP method là lũy đẳng nếu bạn gửi cùng một request 1 lần hay 100 lần thì trạng thái cuối cùng của server vẫn y hệt nhau.
    + `GET, PUT, DELETE` là lũy đẳng (xóa bản ghi id=1 một lần hay nhiều lần thì bản ghi đó vẫn biến mất).
    + `POST` không lũy đẳng (nhấn nút submit 10 lần sẽ sinh ra 10 bản ghi mới).

## IV. HTTP Headers quan trọng & Content Negotiation
- `Content-Type`: Cho biết request body hoặc response body đang chứa loại dữ liệu gì.
- `Accept`: Client báo cho server biết nó mong muốn nhận lại dữ liệu định dạng gì.
- `Authorization`: Gửi thông tin chứng minh danh tính (như Token, API Key).

- **Content Negotiation:** Cơ chế "thỏa thuận" định dạng nội dung giữa client và server thông qua cặp header Accept và Content-Type.
Hoạt động của Content Negotiation: Nếu client gửi request với header Accept: application/xml, server sẽ cố gắng chuyển đổi dữ liệu thành dạng XML và trả về kèm Content-Type: application/xml. Nếu server chỉ hỗ trợ JSON, nó sẽ từ chối bằng lỗi 406 Not Acceptable, hoặc tự fallback trả về application/json tùy cấu hình.

## V. Status Codes mở rộng
- **2xx (Thành công):** `200 OK`, `201 Created`, `204 No Content`.
- **3xx (Chuyển hướng):** `301 Moved Permanently (chuyển URL vĩnh viễn)`, `304 Not Modified (báo client dùng cache)`.
- **4xx (Lỗi Client):** `400 Bad Request (lỗi cú pháp/logic)`, `401 Unauthorized (chưa xác thực)`, `403 Forbidden (đã xác thực nhưng thiếu quyền)`, `404 Not Found`, `405 Method Not Allowed`, `409 Conflict`, `410 Gone`, `415 Unsupported Media Type`, `429 Too Many Requests`.
- **5xx (Lỗi Server):** `500 Internal Server Error (lỗi code crash)`, `502 Bad Gateway`, `503 Service Unavailable`.

- Giải thích:
    - `401 vs 403`: 
        + `401`: hệ thống không biết bạn là ai (chưa đăng nhập hoặc token hết hạn). 
        + `403`: hệ thống biết bạn là ai, nhưng tài khoản của bạn không có quyền thực hiện hành động đó (ví dụ: nhân viên cố xóa dữ liệu của sếp).
    - `405`: Client gọi sai method. Ví dụ URL /students cấu hình chỉ nhận POST, nhưng client lại dùng lệnh PUT.
    - `415`: Client cấu hình sai header. Ví dụ server chỉ nhận JSON, nhưng client lại gửi file lên với Content-Type: text/html.

## VI. Mở rộng Bài 6 thành RESTful (Phân tách PUT/PATCH và Bắt Header)

- File code python: [Restful_B6](/W1/api_session_01/restful_B6.py)
- Link Drive ảnh kết quả test: ["W1\api_session_01\test_results\RESTful_B6_test"](https://drive.google.com/drive/folders/1m6ZvhPj8IJBON1aIjKXUJSRVU3VZhZcn?usp=sharing)
