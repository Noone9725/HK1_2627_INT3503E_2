# Security Audit - UET-Connect API

Tài liệu liệt kê 7 điểm có nguy cơ rò rỉ dữ liệu hoặc bị tấn công trong hệ thống xác thực và phân quyền của API, kèm theo biện pháp khắc phục.

---

## 1. Lộ bài viết riêng tư của người dùng khác qua lỗ hổng BOLA (OWASP API1:2023)
- **Điểm có thể lộ:** Tại endpoint `GET /posts/{id}`, nếu backend chỉ kiểm tra token hợp lệ và có scope `posts:read` mà quên kiểm tra chủ sở hữu của bài viết (`author_id`), User A có thể thay đổi `{id}` tuần tự (123, 124, 125...) để đọc toàn bộ bài viết riêng tư (`is_private = true`) của User B.
- **Cách khắc phục:** 
  + Bổ sung decorator kiểm tra quyền sở hữu đối tượng (`@user_owns_resource`) ở tầng cuối cùng.
  + Chỉ trả về dữ liệu nếu `post.is_private == false` HOẶC `str(post.author_id) == str(current_user.id)` HOẶC `"admin" in current_user.roles`.

## 2. Giả mạo JWT qua lỗi `alg=none` hoặc Algorithm Confusion (HS256 vs RS256)
- **Điểm có thể lộ:** 
  + Kẻ tấn công sửa header của JWT thành `{"alg": "none"}` và xóa chữ ký để vượt qua bước kiểm tra nếu server tin tưởng mù quáng vào trường `alg` do client gửi lên.
  + Hoặc nếu server dùng khóa bất đối xứng `RS256`, kẻ tấn công lấy Public Key công khai của server để ký một token mới với header `alg: "HS256"` khiến server dùng chính Public Key đó làm HMAC secret và xác thực thành công.
- **Cách khắc phục:**
  + Cấu hình danh sách trắng (allowlist) thuật toán cố định ở phía server (ví dụ: `JWT_ALGORITHM="HS256"`), tuyệt đối từ chối token có `alg=none`.
  + Tách biệt khóa ký theo thuật toán, sử dụng secret ngẫu nhiên tối thiểu 256-bit và quản lý qua biến môi trường/Secret Manager.

## 3. Đánh cắp Token phía Client do lưu trữ trong `localStorage` hoặc `sessionStorage`
- **Điểm có thể lộ:** Nếu ứng dụng web frontend lưu `access_token` và `refresh_token` vào `localStorage` hoặc `sessionStorage`, bất kỳ lỗ hổng XSS (Cross-Site Scripting) nào hoặc thư viện JavaScript bên thứ ba bị nhiễm độc trên trang đều có thể gọi `localStorage.getItem('token')` để đánh cắp toàn bộ phiên đăng nhập.
- **Cách khắc phục:**
  + Đối với Web Client: Sử dụng mô hình BFF (Backend-For-Frontend) và lưu token trong Cookie với các cờ bảo mật `HttpOnly`, `Secure`, và `SameSite=Strict/Lax` kết hợp cơ chế chống CSRF.
  + Giới hạn thời gian sống (TTL) của Access Token ngắn (15 phút) để giảm phạm vi thiệt hại (blast radius) nếu bị lộ.

## 4. Rò rỉ thông tin nhạy cảm (PII) trong JWT Payload và API Response (OWASP API3:2023)
- **Điểm có thể lộ:** 
  + Phần Payload của JWT dạng ký (JWS) chỉ được mã hóa Base64url chứ không được mã hóa bảo mật (encryption). Mọi người lấy được token đều có thể giải mã để đọc nội dung bên trong. Nếu đặt email cá nhân, số điện thoại, hoặc mật khẩu vào claims sẽ gây lộ lọt PII.
  + Tại `GET /posts/{id}`, nếu truy vấn DB bằng `SELECT *` và trả thẳng object ra JSON, API có thể làm lộ các trường ẩn của tác giả hoặc cấu trúc nội bộ.
- **Cách khắc phục:**
  + Chỉ đưa các claims tối thiểu vào JWT: `sub` (ID người dùng), `roles`, `scopes`, `iat`, `exp`, `jti`, `iss`, `aud`.
  + Bắt buộc lọc dữ liệu đầu ra qua DTO (`PostDTO`) với danh sách trường được phép hiển thị (whitelist).

## 5. Không thể thu hồi phiên khi lộ Token hoặc sau khi Logout (Thiếu cơ chế Revocation)
- **Điểm có thể lộ:** Vì JWT có tính chất không trạng thái (stateless), nếu người dùng bấm "Đăng xuất" hoặc phát hiện bị lộ token nhưng server chỉ xóa token ở trình duyệt mà không lưu vết ở backend, kẻ tấn công vẫn tiếp tục sử dụng `access_token` và `refresh_token` đã đánh cắp cho đến khi hết hạn tự nhiên (lên tới 30 ngày với Refresh Token).
- **Cách khắc phục:**
  + Gắn mã định danh duy nhất `jti` cho mọi JWT.
  + Triển khai Redis blocklist kiểm tra trạng thái thu hồi (`@jwt.token_in_blocklist_loader`). Khi người dùng logout hoặc xoay vòng (rotate) refresh token, ghi ngay `jti` vào Redis với TTL bằng thời gian sống còn lại của token.

## 6. Lộ danh sách tài khoản (User Enumeration) và Brute-force tại `POST /auth/login` (OWASP API2:2023)
- **Điểm có thể lộ:** 
  + Nếu endpoint `/auth/login` trả về lỗi `"Email không tồn tại"` khi sai email và `"Sai mật khẩu"` khi đúng email, hoặc khi email không tồn tại thì hàm trả về ngay lập tức (1ms) trong khi email tồn tại thì mất 200ms để chạy hàm hash, kẻ tấn công sẽ lập được danh sách email hợp lệ trong hệ thống.
  + Thiếu giới hạn tần suất (Rate-limit) cho phép kẻ tấn công thử hàng vạn mật khẩu bị lộ từ nơi khác (Credential Stuffing).
- **Cách khắc phục:**
  + Luôn trả về cùng một mã lỗi `401 Unauthorized` với nội dung chung `invalid_credentials`.
  + Thực hiện một phép băm giả (dummy hash verification) khi email không tồn tại để cân bằng thời gian phản hồi.
  + Áp dụng Rate-limit theo IP và theo tài khoản, trả về `429 Too Many Requests`.

## 7. Lộ mật khẩu hàng loạt khi Database bị xâm nhập hoặc lộ Token trong Server Log
- **Điểm có thể lộ:** 
  + Lưu mật khẩu dạng văn bản thuần (plaintext) hoặc dùng các hàm băm nhanh như MD5, SHA-1, SHA-256 không có salt khiến kẻ tấn công dễ dàng dò ngược mật khẩu bằng GPU/Rainbow Table nếu lộ DB.
  + Cấu hình middleware ghi log toàn bộ HTTP Request Header (`Authorization: Bearer ...`) hoặc Request Body (`password`) ra file log văn bản.
- **Cách khắc phục:**
  + Sử dụng thuật toán băm mật khẩu chuyên dụng **Argon2id** (với tham số `memory_cost=65536`, `time_cost=3`, `parallelism=4`) hoặc **bcrypt** (cost >= 10).
  + Che (mask/redact) trường `password` và header `Authorization` trong toàn bộ hệ thống ghi log.