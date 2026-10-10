# W4 - Tasks API 

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

## 3. Bài toán:
API Quản lý task nội bộ

1. SourceCodes triển khai:

- OpenAPI Specification đặc tả cho API:
[openapi.yaml](/W4/tasks-api/openapi.yaml) 

- App triển khai Swagger UI có Database on Ram test thực thi và có tách `/openapi.json` cho Specification + `/docs` cho Swagger UI:
[app.py](/W4/tasks-api/app.py)

2. Thực hiện test Local:

- Khởi động app:
   ```bash
   python app.py
   ```

- Truy cập xem Specification(json): [openapi](http://localhost:5000/openapi.json)

- Truy cập Swagger UI và test: [UI](http://localhost:5000/docs)

3. 2 quyết định thiết kế khó nhất (Trade-offs) trong API này:

- **Thực hiện Validation thủ công ở backend để bảo vệ dữ liệu đầu vào**
   + **Quyết định:** Tự viết các điều kiện `if/else` ở Backend để kiểm tra định dạng ngày (chuẩn ISO 8601: `YYYY-MM-DD`) và các giá trị Enum (`status`, `priority`) sau đó trả về mã lỗi `422 ValidationError`, thay vì để mặc định.
   + **Trade-off:** Sử dụng `flasgger` để đúng hướng Spec-first (đọc trực tiếp từ file `openapi.yaml`), nhưng nó không tự động chặn dữ liệu rác từ Swagger UI. Chấp nhận Backend phải thêm code xử lý logic kiểm tra thủ công để an toàn của dữ liệu, thay vì phải cài thêm các thư viện phức tạp như `flask-smorest` hay `marshmallow`.

- **Tách biệt hoàn toàn các Schema (CreateTaskInput, UpdateTaskInput, Task)**
   - **Quyết định:** Thay vì dùng chung một schema `Task` cho tất cả các endpoint, viết tách hẳn ra làm 3 schema riêng biệt cho POST (CreateTaskInput), PATCH (UpdateTaskInput) và response (Task) trả về.
   - **Trade-off:** Làm file `openapi.yaml` dài ra đáng kể, mỗi khi muốn thêm một trường mới (như `dueDate`), phải nhớ update thủ công ở cả 3 nơi, dễ sót. Nhưng API chặt chẽ và an toàn hơn: POST sẽ chặn không cho Frontend tự gửi `id` hay ép `status` (tạo mới mặc định phải là `open`), PATCH cho phép gửi các trường tùy ý để cập nhật, còn response GET thì luôn trả về đầy đủ thông tin.

4. Các Ảnh Test:

---

- **POST:**

![W4_POST_201](https://github.com/user-attachments/assets/8e7ecb18-8595-4f45-a376-4f7e694c50e5)

*Hình 1: Test W4_POST_201*

![W4_POST_400](https://github.com/user-attachments/assets/65ea3e1b-b5fa-4f59-80fa-93391f32392e)

*Hình 2: Test W4_POST_400*

![W4_POST_422_Date](https://github.com/user-attachments/assets/66801fb7-d9bc-42d4-b658-9d38a76eaecd)

*Hình 3: Test W4_POST_422_Date

![W4_POST_422_Priority](https://github.com/user-attachments/assets/d4bf8a5e-dd53-4dc7-89e2-0d3a23597575)

*Hình 4: Test W4_POST_422_Priority*

---

- **GET list:**

![W4_GET_list_200](https://github.com/user-attachments/assets/345a53c8-c386-4ce8-98bd-64d1f459bd10)

*Hình 5: Test W4_GET_list_200*

---

- **GET id:**

![W4_GET_id_200](https://github.com/user-attachments/assets/a16847f2-ef4f-4498-8282-1915de90c3ed)

*Hình 6: Test W4_GET_id_200*

![W4_GET_id_404](https://github.com/user-attachments/assets/7846b248-4703-43b9-95f5-3e1bbdb3a3f0)

*Hình 7: Test W4_GET_id_404*

---

- **PATCH:**

![W4_PATCH_200](https://github.com/user-attachments/assets/92bc49ec-1afb-400d-810b-0fe5b6bc2e09)

*Hình 8: Test W4_PATCH_200*

![W4_PATCH_400](https://github.com/user-attachments/assets/ffab6897-98cb-4ee2-beb7-ea99a679cab4)

*Hình 9: Test W4_PATCH_400*

![W4_PATCH_404](https://github.com/user-attachments/assets/dae8e9e0-872d-47fa-b3b9-ac351aa4ecec)

*Hình 10: Test W4_PATCH_404*

![W4_PATCH_422_Status](https://github.com/user-attachments/assets/7d517191-9d7b-4627-94db-803b812d7cdb)

*Hình 11: Test W4_PATCH_422_Status*

---

- **DELETE:**

![W4_DELETE_204](https://github.com/user-attachments/assets/21bc9872-30fc-41be-8ed0-16cfc4b169af)

*Hình 12: Test W4_DELETE_204*

---
