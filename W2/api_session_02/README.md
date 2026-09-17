# W2 - API Session 02

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
![W2_B1_GET_200](https://github.com/user-attachments/assets/6a158998-63cc-4d3e-a396-66c184307573)
*Hình 1: Test GET_200_OK B1*

![W2_B1_POST_201](https://github.com/user-attachments/assets/1c6856a7-4706-442f-87b8-c68ba18945b4)
*Hình 2: Test POST_201_CREATED B1*

![W2_B1_POST_422](https://github.com/user-attachments/assets/7f3dcf34-fc99-493a-86d8-65ecb3c3c339)
*Hình 3: Test POST_422_UNPROCESSABLE_ENTITY B1*

![W2_B1_POST_415](https://github.com/user-attachments/assets/6d8fb8be-6825-424a-810c-0840f8092ff3)
*Hình 4: Test POST_415_UNSUPPORTED_MEDIA_TYPE B1*

### Bài 2:
![W2_B2_PATCH_200](https://github.com/user-attachments/assets/71c48bd1-4592-43bf-afdb-866f8a4c2816)
*Hình 5: Test PATCH_200_OK B2*

![W2_B2_PUT_200](https://github.com/user-attachments/assets/543ab9e1-ab29-496b-9690-cd0bf8c1c8c1)
*Hình 6: Test PUT_200_OK B2*

![W2_B2_DELETE_204](https://github.com/user-attachments/assets/337a05ba-b5fe-4a51-83c9-529e39abb690)
*Hình 7: Test DELETE_204_NO_CONTENT B2*

### Bài 3:
![W2_B3_GET_400](https://github.com/user-attachments/assets/c4e5ea95-bbc5-4177-ad63-29aeb484ed65)
*Hình 8: Test GET_400_BAD_REQUEST B3*

![W2_B3_GET_Page_200](https://github.com/user-attachments/assets/c7994ba8-19f5-48b5-ab10-52f4fba0ba5f)
*Hình 9: Test GET_Page_200_OK B3*

![W2_B3_GET_Aut_200](https://github.com/user-attachments/assets/7606a037-ec2c-4ea8-b026-062aab4acbb6)
*Hình 10: Test GET_Aut_200_OK B3*

![W2_B3_GET_Title_200](https://github.com/user-attachments/assets/8ca67f80-62c3-4daf-92b1-394cfca82149)
*Hình 11: Test GET_Title_200_OK B3*
