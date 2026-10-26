# UET-Connect API Social-Network with 3 Auth endpoint

## 1. Xác định dự án API Social-Network
---

- **Tên dự án:** `UET-Connect API` — Hệ thống mạng xã hội chia sẻ bài viết học thuật nội bộ.
- **Đối tượng sử dụng (Role):** 
    + Sinh viên (`user`)
    + Quản trị viên (`admin`).   
- **Tài nguyên cốt lõi (Resource):**
    + Tài khoản người dùng (`users`)
    + Bài viết (`posts`): với hai trạng thái hiển thị là *công khai* (`is_private: false`) hoặc *riêng tư* (`is_private: true`).

- 3 endpoint cần xây dựng (`BTVN`):
    + `POST /auth/login`: Xác thực *email/mật khẩu*, trả về cặp *Access Token* và *Refresh Token*.   
    + `POST /auth/refresh`: Nhận *Refresh Token* hợp lệ để cấp *Access Token* mới.   
    + `GET /posts/{id}`: Xem chi tiết một bài viết dựa trên id

---

## 2. Phân tích cơ chế Auth và rủi ro bảo mật với 3 luồng Endpoint
---

- Luồng `POST /auth/login`:
    + **Rủi ro:** Tấn công vét cạn mật khẩu (Brute-force / Credential Stuffing) và dò tài khoản thông qua sự khác biệt của thông báo lỗi hoặc thời gian phản hồi (Timing Attack).   
    + **Cách giải quyết:** Luôn kiểm tra mật khẩu bằng thư viện `argon2-cffi`, trả về duy nhất một thông báo lỗi chung `401 Unauthorized (invalid_credentials)` dù sai email hay sai mật khẩu, và áp dụng giới hạn tần suất gọi API (Rate-limit) trả về `429 Too Many Requests`.   

- Luồng `POST /auth/refresh`:
    + **Rủi ro:** Tấn công lấy cắp Refresh Token để duy trì quyền truy cập trái phép lâu dài, hoặc dùng Access Token giả làm Refresh Token, hoặc quyền hạn của user trong DB đã bị hủy nhưng token mới vẫn giữ quyền cũ.   
    + **Cách giải quyết:** Bắt buộc kiểm tra loại token phải là refresh token, đối chiếu `jti` với Redis blocklist để đảm bảo token chưa bị thu hồi, và truy vấn lại database (`load_permissions`) để nạp lại `roles` cùng `scopes` mới nhất vào Access Token mới.   

- Luồng `GET /posts/{id}`:
    + **Rủi ro:** 
        + Rủi ro **OWASP API1:2023 - BOLA (Broken Object Level Authorization):** xảy ra khi User A dùng token hợp lệ có quyền `posts:read` nhưng truyền `id` bài viết riêng tư của User B để đọc dữ liệu trái phép. 
        + Rủi ro **OWASP API3:2023 (Broken Object Property Level Auth):** nếu API trả nguyên dòng dữ liệu thô từ DB làm lộ thông tin nhạy cảm của tác giả.   
    + **Cách giải quyết:** Thực thi 3 lớp kiểm tra tuần tự: 
        + (1) Xác minh chữ ký JWT, thuật toán trong allowlist, hạn `exp`, và `jti` không nằm trong blocklist; 
        + (2) Kiểm tra token có chứa scope `posts:read`; 
        + (3) Nếu bài viết có `is_private == true`, bắt buộc kiểm tra `post.author_id == current_user.id` hoặc `"admin" in current_user.roles`. Dữ liệu trả về phải được lọc qua DTO.

- Thực hiện:
    + **Xác thực (AuthN):** Lưu mật khẩu bằng thuật toán băm **Argon2id** (có salt và cấu hình memory-hard). Khi đăng nhập thành công, hệ thống cấp **JWT** ký bằng thuật toán HS256 gồm Access Token có thời hạn ngắn (15 phút = 900 giây) và Refresh Token có thời hạn dài (30 ngày = 2592000 giây).   
    + **Phân quyền (AuthZ):** Kết hợp **RBAC** (`roles`: `user`, `admin`), **Scope** (`posts:read`, `posts:write`) lưu trong claims của JWT và Ownership (kiểm tra `author_id` của bài viết).   
    + **Quản lý phiên và thu hồi (Revocation):** Mỗi JWT mang một mã định danh duy nhất `jti`. Khi người dùng đăng xuất hoặc làm mới token, `jti` cũ được đưa vào Redis blocklist để vô hiệu hóa tức thì. 

---

## 3. Thiết kế spec cho 3 Endpoint
---

- `POST /auth/login`:
    + **Cơ chế Auth & Scope yêu cầu:**
        Public (Không cần token, không cần scope).
    + **HTTP Status Code & Error Code & Tình huống xảy ra:**
        + `200 OK`: Đăng nhập thành công, trả về `access_token` và `refresh_token`.
        + `400 Bad Request`: `invalid_request`: Thiếu trường `email/password` hoặc sai định dạng JSON.
        + `401 Unauthorized`: `invalid_credentials`: Sai email hoặc sai mật khẩu (thông báo chung).
        + `429 Too Many Requests`: `rate_limit_exceeded`: Gửi quá nhiều yêu cầu đăng nhập trong thời gian ngắn.

- ``POST /auth/refresh`:
    + **Cơ chế Auth & Scope yêu cầu:**
        + Bearer Auth (Refresh Token).
        + Scope: Không yêu cầu scope nghiệp vụ nhưng claim phải là Refresh Token.
    + **HTTP Status Code & Error Code & Tình huống xảy ra:**
        + `200 OK`: Làm mới thành công, trả về `access_token` mới.
        + `401 Unauthorized`: `invalid_or_expired_token`: Thiếu header Bearer, sai chữ ký, hết hạn `exp`, truyền nhầm Access Token, hoặc `jti` đã bị thu hồi trong Redis blocklist.
        + `429 Too Many Requests`: `rate_limit_exceeded`: Gọi refresh vượt ngưỡng giới hạn.

- `GET /posts/{id}`
    + **Cơ chế Auth & Scope yêu cầu:**
        + Bearer Auth (Access Token).
        + Scope bắt buộc: `posts:read`.
        + Policy: Ownership nếu bài viết riêng tư.
    + **HTTP Status Code & Error Code & Tình huống xảy ra:**
        + `200 OK`: Trả về thông tin bài viết thông qua DTO.
        + `401 Unauthorized`: `unauthorized`: Không gửi token, token hết hạn, sai chữ ký/`iss`/`aud`, hoặc `jti` nằm trong blocklist.
        + `403 Forbidden`: 
            + `insufficient_scope`: Token hợp lệ nhưng thiếu scope `posts:read`.
            + `forbidden`: Bài viết là `private` và người gọi không phải chủ sở hữu (`author_id != sub`) và cũng không có role `admin`.
        + `404 Not Found`: `not_found`: Bài viết với id được yêu cầu không tồn tại.

- Phân biệt mã lỗi:
    + `401 Unauthorized`: dành riêng cho lỗi xác thực danh tính (AuthN thất bại: chưa đăng nhập, token hỏng, hết hạn hoặc bị thu hồi). 
    + `403 Forbidden`: dành riêng cho lỗi phân quyền (AuthZ thất bại: đã biết người gọi là ai nhưng thiếu scope `posts:read` hoặc vi phạm quyền sở hữu đối tượng BOLA).

- Cấu trúc JWT Claims thiết kế:
    + **Header:** `{"alg": "HS256", "typ": "JWT", "kid": "key-2026-01"}`.   
    + **Payload:**` {"iss": "uet-connect-auth", "aud": "uet-connect-api", "sub": "42", "jti": "uuid-v4", "iat": 1724008400, "exp": 1724009300, "roles": ["user"], "scopes": ["posts:read", "posts:write"]}`.

---

## 4. OpenAPI Spec cho 3 Endpoint
---

[OpenAPI Spec](/W6/openapi_spec/openapi.yaml)

---

## 5. Tài liệu SecurityAudit.md
---

[Security Audit](/W6/SecurityAudit.md)

---