# W5 - Bookstore API

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
   curl.exe <request>
    ```
- Linux/Mac:
   ```bash
   $ curl <request>
    ```

## 3. Bài toán:

Thiết lập dự án API bằng Flask, định nghĩa data model (Book, Author) với SQLAlchemy, xây dựng resource structure (JSON Schema) và các route cơ bản (CRUD).

Phiên bản v1 hiện tại chỉ có resource structure của books với triển khai đơn giản.

1. Book Resource:
- [book_schema](/W5/bookstore-api/schemas/book.json)
- [book_route](/W5/bookstore-api/routes/books.py)

4. Ảnh test tương tác với Book Resource

- **POST:** Tạo dữ liệu mẫu vào Database

![W5_POST_DB](https://github.com/user-attachments/assets/c2f62e8e-a69c-429f-bc87-f527783f33f4)

*Hình 1: W5_POST_DB*

- **GET:** Test phân trang, filter và sort

+ **Offset:**

![W5_GET_Offset](https://github.com/user-attachments/assets/d646c57f-1fc1-4e31-ba39-b9fe1c05361c)

*Hình 2: W5_GET_Offset*

+ **Cursor Page 1:**

![W5_GET_Cursor_P1](https://github.com/user-attachments/assets/32f7b08d-cbda-4b31-8fbe-602c8ec4232e)

*Hình 3: W5_GET_Cursor_P1*

+ **Cursor Page 1:**

![W5_GET_Cursor_P2](https://github.com/user-attachments/assets/5a03b4f1-0905-4026-9f89-6f7232382feb)

*Hình 4: W5_GET_Cursor_P2*

- **PUT:** Cập nhật dữ liệu

![W5_PUT](https://github.com/user-attachments/assets/92fac9a2-a11c-4346-bb8a-d988d69eb91a)

*Hình 5: W5_PUT*

- **DELETE:** Xóa dữ liệu

![W5_DELETE](https://github.com/user-attachments/assets/9beebbee-07fd-4818-930c-cb928fdb52ac)

*Hình 6: W5_DELETE*
