# W7 - Backend Service
Bài thực hành lab1, hoàn thiện theo cách tiếp cận Code-First

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
4. Thiết lập Database:
    ```bash
    flask db init
    flask db migrate -m "init"
    flask db upgrade
    ```
5. Chạy Server:
    ```bash
    flask run --reload
    ```
6. Truy cập Swagger UI:
    [Swagger UI](http://127.0.0.1:5000/swagger-ui)     
7. Chạy Test:
- Chạy lệnh:
    ```bash
    curl.exe -X <request>
    ```
- Hoặc thực hiện **"Try it out"** trên Swagger UI

## 3. Hình ảnh kết quả:

1. Swagger UI:

![Swagger_UI](https://github.com/user-attachments/assets/a632ae62-6280-4e72-88d4-46f1c59275b0)

*Hình 1: Swagger UI*

2. Test CRUD Products:

![Test_CRUD_Products](https://github.com/user-attachments/assets/58adb748-06fa-47ba-8494-82f88720a7a9)

*Hình 2: Test CRUD Products*

3. Test CRUD Orders:

![Test_CRUD_Orders](https://github.com/user-attachments/assets/7748f384-bed3-4684-8efd-1e11bfbea972)

*Hình 3: Test CRUD Orders*

4. Test Health Check:

![Health_Check](https://github.com/user-attachments/assets/5afb5f2e-9f7b-4b49-93c3-9b01503ff9e7)

*Hình 4: Test Health Check*

5. Khởi tạo và chạy toàn bộ hệ thống với Docker:

![Docker_Build](https://github.com/user-attachments/assets/585f4546-b3d9-48c8-8083-6b2e6ea07481)

*Hình 5: Test Docker Build*

6. Pytest orders với Docker:

![pytest_orders](https://github.com/user-attachments/assets/eb154a14-b8af-457b-99ee-209e91584ff1)

*Hình 6: pytest orders*