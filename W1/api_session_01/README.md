# W1 - API Session 01

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

## 3. Ảnh Test:

### Bài 1:
![W1_B1_200](https://github.com/user-attachments/assets/f8271755-e97a-4404-a42a-233d1610e42d)
*Hình 1: Test message_200_OK B1*

### Bài 2:
![W1_B2_health(GET)_200](https://github.com/user-attachments/assets/90983131-f052-4863-90df-1a2027ae0800)
*Hình 2: Test health(GET)_200_OK B2*

![W1_B2_echo(POST)_200](https://github.com/user-attachments/assets/58e64bf0-b41d-41b7-a6c3-ffa6a8a3c544)
*Hình 3: Test echo(POST)_200_OK B2*

### Bài 3:
![W1_B3_POST_201](https://github.com/user-attachments/assets/fda74fee-2e0f-46f9-9e5e-cbdc03095cc9)
*Hình 4: Test POST_201_CREATED B3*

![W1_B3_POST_400](https://github.com/user-attachments/assets/fcbdfbef-48ea-4d21-844f-c82b04ea4137)
*Hình 5: Test POST_400_BAD_REQUEST B3*

### Bài 4:
![W1_B4_Path_params](https://github.com/user-attachments/assets/775de47c-cd31-4d10-ae8d-fa6172bb952f)
*Hình 6: Test GET_Path_params B4*

![W1_B4_Query_string](https://github.com/user-attachments/assets/0f3ef9d4-6718-40a7-8735-74226f60d190)
*Hình 7: Test GET_Query_string B4*

### Bài 5:
![W1_B5_DELETE](https://github.com/user-attachments/assets/42b37483-df64-4f3d-a1d0-af512d19c3b3)
*Hình 8: Test DELETE B5*

### Bài 6:
![W1_B6_GET_List](https://github.com/user-attachments/assets/1a88a3f1-6d51-4308-a903-398305ded46e)
*Hình 9: Test GET_List B6*

![W1_B6_POST](https://github.com/user-attachments/assets/b47fd304-ae42-4ed2-b6e9-d13fc5bb8f4a)
*Hình 10: Test POST B6*

![W1_B6_PUT](https://github.com/user-attachments/assets/3d917001-931d-444d-bb5f-3aa7887888c6)
*Hình 11: Test PUT B6*

![W1_B6_DELETE](https://github.com/user-attachments/assets/37f4c6dc-c844-4235-9432-cce43d51c02c)
*Hình 12: Test DELETE B6*
