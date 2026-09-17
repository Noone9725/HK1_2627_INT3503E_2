## Bài 1: 3 API public thực tế

### 1. GitHub REST API
- **Loại API:** REST.
- **Base URL:** [https://api.github.com](https://api.github.com)
- **Auth method:** Personal Access Token (Bearer Token) hoặc OAuth 2.0.
- **Versioning:** Có (được chỉ định qua header Accept, ví dụ: application/vnd.github+json kết hợp với header X-GitHub-Api-Version: 2022-11-28).
- **Resource identifier:** Số nguyên (ID của repository, ID của user).

### 2. Spotify Web API
- **Loại API:** REST.
- **Base URL:** [https://api.spotify.com/v1](https://api.spotify.com/v1)
- **Auth method:** OAuth 2.0 (Access Token truyền qua header Authorization: Bearer).
- **Versioning:** Có (được nhúng trực tiếp vào URL: /v1).
- **Resource identifier:** Base62 string (Chuỗi đặc trưng của Spotify, ví dụ: 4aawyAB9vmqN3pzPSRcl4d).

### 3. OpenWeather API
- **Loại API:** REST.
- **Base URL:** [https://api.openweathermap.org/data/2.5](https://api.openweathermap.org/data/2.5)
- **Auth method:** API Key (truyền thẳng qua query string URL, ví dụ: ?appid=YOUR_API_KEY).
- **Versioning:** Có (nhúng trong URL: /2.5).
- **Resource identifier:** Số nguyên (ID của thành phố).

## Bài 2: So sánh đặc điểm API tốt Higginbotham Ch.1 + Geewax Ch.1 với bài giảng

### 1. Các điểm chung:
- Cả Higginbotham và Geewax cũng đều cho rằng API là một `Hợp đồng rõ ràng (Contract-first)` giữa client và server, đóng vai trò giấu đi các `Cài đặt nội bộ (Abstraction)`.
- Cũng thống nhất với tính `Có thể tái sử dụng` và `Độc lập với ngôn ngữ và nền tảng` trong slide: API sinh ra để phục vụ nhiều loại client khác nhau mà không bị bó buộc công nghệ.

### 2. Các điểm bổ sung:
- **1:** Higginbotham nhấn mạnh vào khái niệm `Developer Experience (DX)`: một API xuất sắc không chỉ đúng về mặt kỹ thuật mà phải dễ học, dễ dùng và có tài liệu (documentation) trực quan.
- **2:** Geewax tập trung vào tính `Nhất quán (Consistency)`. Toàn bộ hệ thống API phải tuân theo một tiêu chuẩn thống nhất về cách đặt tên, URL, cấu trúc response và mã lỗi để client có thể dự đoán (predictable) cách gọi mà không cần đọc lại tài liệu liên tục.
- **3:** Sách bổ sung yếu tố `Security by design`, API cần được thiết kế với tư duy bảo mật (như rate limiting, phân quyền) ngay từ giai đoạn lên cấu trúc tài nguyên, không chỉ đơn thuần là `versioning và quan sát được (Observable)` như liệt kê trong slide.

## Bài 3: Hoàn thiện Bài 6 + Bổ sung

### File code python: 
[Upgades_B6](/W1/api_session_01/upgrades_B6.py)

### Ảnh Test:

![W1_UB6_(a)_GET_SearchTitle](https://github.com/user-attachments/assets/ada27dd1-13d7-4528-84f3-5fc23df7577e)
*Hình 1: Test GET_SearchTitle_200_OK UB6*

![W1_UB6_(a)_GET_SortTitle](https://github.com/user-attachments/assets/485780b3-b4bc-4811-93dd-8368996467a6)
*Hình 2: Test GET_SortTitle_200_OK UB6*

![W1_UB6_(c)_POST_201](https://github.com/user-attachments/assets/d34333d6-51bd-4447-8da2-b8188470ddd5)
*Hình 3: Test POST_201_CREATED UB6*

![W1_UB6_(c)_POST_400](https://github.com/user-attachments/assets/af698bbd-23e6-4333-b77c-db3510aaa01a)
*Hình 4: Test POST_400_BAD_REQUEST UB6*

![W1_UB6_(c)_PUT](https://github.com/user-attachments/assets/f8543f23-83f0-418d-850b-0a65d8d7172e)
*Hình 5: Test PUT UB6*