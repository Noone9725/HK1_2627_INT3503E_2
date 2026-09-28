# W3 - API Design

## 1. Yêu cầu hệ thống:
- Python >= 3.10

## 2. Thiết lập và chạy:

1. Kích hoạt môi trường ảo:
- Windows: 
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
- Linux/Mac: 
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
    ```
3. Cài đặt thư viện (flask):
   ```bash
   pip install -r requirements.txt
   # Kiểm tra:
   flask --version
   ```

4. Khởi động file python theo bài tương ứng:
   ```bash
   python <Bài số x>.py
   ```

5. Mở terminal khác và test với `curl` (theo ví dụ trong các ảnh kết quả)
- Windows: 
   ```bash
   cmd.exe /c 'curl.exe <request>'
    ```
- Linux/Mac:
   ```bash
   $ curl <request>
    ```

## 3. Các bài toán:

### Lab 1: Thiết kế resource cho Blog API

#### BÀI TOÁN
Nền tảng blog đơn giản:
Một blog cho phép người dùng đăng bài viết (posts), mỗi bài có bình luận (comments) và gắn thẻ (tags). Mỗi user có hồ sơ và đăng ký theo dõi (follow) tác giả khác. Hãy thiết kế cấu trúc endpoint đầy đủ.

#### THIẾT KẾ
1. Xác định resources trong miền
- `users`: Người dùng nền tảng.
- `posts`: Bài viết trên blog.
- `comments`: Bình luận của bài viết.
- `tags`: Thẻ phân loại bài viết.
2. Phân loại collection / item / sub-resource
- **Collection:** `/users`, `/posts`, `/tags`.
- **Item:** `/users/{id}`, `/posts/{id}`, `/tags/{id}`.
- **Sub-resource**: `/users/{id}/profile`, `/users/{id}/followers`, `/users/{id}/following`, `/posts/{id}/comments`, `/posts/{id}/tags`.
3. Vẽ sơ đồ cây endpoint và quyết định version segment
```
/api/v1
├── /users
│   ├── /{id}
│   │   ├── /profile
│   │   ├── /followers
│   │   └── /following
├── /posts
│   ├── /{id}
│   │   ├── /comments
│   │   │   └── /{comment_id}
│   │   └── /tags
├── /tags
    └── /{id}
```
4. Triển khai Flask routes cho collection `/posts` 
SourceCodes:
[Lab1](/W3/api_design/Lab1.py)

#### ẢNH TEST

![W3_L1_GET](https://github.com/user-attachments/assets/9401a5f1-5d5f-4bab-8e5f-8f2df91b2ef5)
*Hình 1: Test W3_L1_GET_200_OK*

![W3_L1_POST](https://github.com/user-attachments/assets/d255727e-d6af-4b2c-bf67-b4bd9ca62749)
*Hình 2: Test W3_L1_POST_201_CREATED*

![W3_L1_GET_id](https://github.com/user-attachments/assets/7daa938b-1d98-46c4-b63f-c42c6b93a419)
*Hình 3: Test W3_L1_GET_id_200_OK*

![W3_L1_PUT](https://github.com/user-attachments/assets/af00dbf7-29c2-415a-9dc3-6c11d417908a)
*Hình 4: Test W3_L1_PUT_200_OK*

![W3_L1_DELETE](https://github.com/user-attachments/assets/692c0074-fb28-436d-a096-b24c8a4f19bd)
*Hình 5: Test W3_L1_DELETE_204_NO_CONTENT*

### Lab 2: Error handler trả về problem+json
#### Bài tập: 
viết một Flask error handler thống nhất trả về problem+json, kèm exception class
#### Gợi ý:
- định nghĩa ProblemError(Exception),
- decorator @app.errorhandler(ProblemError), và
- một handler fallback cho HTTPException

#### SourceCodes:
[Lab2](/W3/api_design/Lab2.py)

#### Kiểm thử:
- request tới /resources/{id} phải trả 404, status code HTTP là 404.

![W3_L2_GET_id](https://github.com/user-attachments/assets/b64b634f-df46-431a-801e-273924b1d06e)
*Hình 1: Test W3_L2_GET_id_404_NOT_FOUND*

- body có type/title/detail/status/instance, không lộ stack trace.
- Nếu gặp exception chưa bắt, trả 500 với message trung tính và log chi tiết server-side.

![W3_L2_Hide_StackTrace](https://github.com/user-attachments/assets/9a3e8f1e-0377-40c3-a721-5a780d07e70d)
*Hình 2: Test W3_L2_Hide_StackTrace_500_INTERNAL_SERVER_ERROR*

- Nếu thiếu Accept hoặc client Accept JSON, vẫn trả problem+json cho lỗi API.

![W3_L2_AcceptMissed](https://github.com/user-attachments/assets/286ad7c9-a5ab-4624-8547-99329ebd64db)
*Hình 3: Test W3_L2_AcceptMissed_400_BAD_REQUEST*

![W3_L2_AcceptHTML](https://github.com/user-attachments/assets/f2f0f5a1-ae74-4ed0-8fb0-6dcbdae39fee)
*Hình 4: Test W3_L2_AcceptHTML_404_NOT_FOUND*

### Lab 3: Triển khai /orders có cursor pagination 
#### Yêu cầu:
GET /orders với
(1) cursor;
(2) filter: status, customer_id;
(3) sort;
(4) sparse fieldsets.

#### SourceCodes:
[Lab3](/W3/api_design/Lab3.py)

#### Kiểm thử:

- Lọc theo status: curl 'localhost:5000/orders?status=paid'

![W3_L3_GET_status](https://github.com/user-attachments/assets/eab2f6c6-477f-44f0-a38d-ea54c437cc79)
*Hình 1: Test W3_L3_GET_status=paid_200_OK*

- Giới hạn 5: curl 'localhost:5000/orders?limit=5'

![W3_L3_GET_limit](https://github.com/user-attachments/assets/405571ac-13cc-49fd-b4e7-b087f98e6ce7)
*Hình 2: Test W3_L3_GET_limit_200_OK*

- Chọn trường trả về: curl 'localhost:5000/orders?fields=id,total'

+ 200 OK:
![W3_L3_GET_fields_OK](https://github.com/user-attachments/assets/ca5c9193-fbc3-4120-85a7-070db67c6169)
*Hình 3: Test W3_L3_GET_fields_200_OK*
    
+ 400 BAD REQUEST:
![W3_L3_GET_fields_ERROR](https://github.com/user-attachments/assets/6a738bd3-d01b-4e0d-a506-2f52af02cf57)
*Hình 4: Test W3_L3_GET_fields_400_BAD_REQUEST*

- Lấy trang tiếp theo bằng cursor: Giả sử next_cursor trả về từ lệnh limit=5 là "NQ==" tức là ID=5

![W3_L3_GET_NextCursor](https://github.com/user-attachments/assets/49f52ab1-7666-4886-aa86-f0eaba2c9d49)
*Hình 5: Test W3_L3_GET_NextCursor_200_OK*

- Kiểm thử cursor hỏng:

![W3_L3_GET_CursorError_400](https://github.com/user-attachments/assets/4e072778-51a9-4c9c-9252-d382a185f584)
*Hình 6: Test W3_L3_GET_CursorError_400_BAD_REQUEST*
