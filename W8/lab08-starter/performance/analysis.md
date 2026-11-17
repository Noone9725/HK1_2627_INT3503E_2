# Lab 4 — Phân tích kết quả

| Kịch bản | Users | Spawn rate | Duration | p95 (ms) | Failure rate | RPS |
|---|---:|---:|---:|---:|---:|---:|
| A | 10 | 2 | 30s | 22 | 0.00 | 4.76 |
| B | 50 | 5 | 60s | 24 | 0.05 | 23.05 |
| C | 200 | 50 | 30s | 55 | 0.24 | 98.26 |

1. Kịch bản có p95 cao nhất là gì? Dùng số liệu quan sát để giải thích.

- **Kịch bản C** (200 users, spawn rate 50/s) có p95 cao nhất đạt 55 ms (so với 22 ms ở Kịch bản A và 24 ms ở Kịch bản B).
- **Nguyên nhân:**
    + *Tranh chấp hàng đợi (Queueing delay):* Server sử dụng Flask development server đơn tiến trình. Từ 10 lên 50 users, độ trễ p95 tăng chậm (22 ms -> 24 ms) do server vẫn xử lý kịp thời, nhưng khi tăng mạnh lên 200 users (spawn rate 50 users/giây), throughput vọt lên 98.26 RPS khiến các request bắt đầu phải xếp hàng chờ trong backlog socket.
    + *Tranh chấp khóa tệp SQLite (File lock):* SQLite chỉ cho phép một transaction ghi duy nhất tại một thời điểm. Tác vụ POST /books khi có nhiều user gọi đồng thời buộc Database phải khóa tệp, đẩy độ trễ ở nhóm 5% request chậm nhất (p95) tăng lên mạnh.

2. Endpoint nào tăng failure rate? Phân biệt lỗi HTTP thực và lỗi đánh dấu trong Locust.

- **Theo quan sát:**
    + Duy nhất endpoint `GET /books?year=[year]` phát sinh lỗi và làm tăng failure rate tổng từ 0.00% (A) -> 0.05% (B) -> 0.24% (C).
    + Tất cả các endpoint còn lại đều đạt Failure rate = 0% trên cả 3 kịch bản, chứng minh server Flask không hề bị quá tải hay ném lỗi HTTP thực tế nào.
- **Nguyên nhân (Dựa trên `locustfile.py`):**
    + Task `search_by_year` được chủ động cài đặt tỷ lệ lỗi giả lập dưới `1%`, trọng số task này là chiếm 25% tổng lượng request:
    ```python
    if random.random() < 0.01:
                response.failure("Simulated 500: Artificial client-side error (1% fail rate)")
    ```
    + Failure rate tăng dần theo số user (A -> C) do quy luật số lớn, khi số user tăng làm số requests tổng tăng theo khiến xác suất sinh task lỗi giả lập này tăng theo (đến kịch bản C là đủ lớn cho xác suất lỗi gần khớp giả lập `1%`).
- **Phân biệt lỗi:**
    + *Lỗi HTTP thực từ server:* `0%`. Mã HTTP trả về từ server luôn là 200 OK.
    + *Lỗi ghi nhận trong báo cáo:* `100%` là client-side evaluation của Locust. Locust chặn response 200 và tự động đánh dấu là failure theo logic random 1% của client test script nhằm mục đích kiểm thử khả năng theo dõi lỗi trên dashboard.
        
3. Với SLO giả định p95 < 300 ms, kịch bản nào đạt? Nêu giới hạn của phép đo.

- **Đánh giá SLO:** Cả 3 kịch bản đều đạt yêu cầu SLO p95 < 300 ms (Kịch bản C cao nhất cũng chỉ dừng ở mức 55 ms, thấp hơn rất nhiều so với ngưỡng 300 ms).
- **Giới hạn phép đo:** 
    + Thử nghiệm được thực hiện trên môi trường máy cá nhân (`localhost`) với Flask dev server và SQLite in-file.
    + Không có: 
        + Độ trễ mạng thực tế (`network latency`) 
        + Cấu hình phân tải (`Load Balancer` / `Reverse Proxy`). 
    + Kết quả này chỉ có giá trị làm baseline so sánh logic code, không thể dùng khẳng định năng lực Production.
- **Đề xuất baseline cho CI Performance Gate:**
    + *Kịch bản chạy kiểm thử tự động trong CI:* Chọn cấu hình tương đương Kịch bản B (`-u 50 -r 5 -t 30s`).
    + *Tiêu chí chặn (Quality Gate):*
        + `p95 <= 100 ms` (ngưỡng an toàn thực tế trên môi trường runner).
        + `Failure rate <= 0.5%` (để dung sai cho `1%` lỗi giả lập của `search_by_year` và loại trừ lỗi mạng nội bộ).

4. Nếu connection pool bị giới hạn ở 5, bạn sẽ kiểm chứng ảnh hưởng như thế nào?

- **Khi 200 người dùng truy cập đồng thời mà SQLAlchemy Connection Pool chỉ cấp tối đa 5 kết nối, theo lý thuyết:**
    + Tại một thời điểm chỉ có tối đa 5 request được mượn kết nối Database để thực thi truy vấn.
    + 195 request còn lại buộc phải xếp hàng chờ trong pool queue.
    + Khi thời gian chờ vượt quá thời hạn timeout của pool (`pool_timeout`), SQLAlchemy sẽ ném lỗi: `TimeoutError: ..., connection timed out`.
    + **Hậu quả:** Server sẽ lập tức trả về lỗi HTTP 500 thực, failure rate sẽ tăng vọt do timeout.

- **Xác nhận bằng Locust:**
    + *Import `QueuePool` trong `app.py`:* (Do test bằng SQLite, cần ép SQLAlchemy dùng `QueuePool`)
    + *Thiết lập giới hạn pool trong `app.py`:*
    ```python
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "poolclass": QueuePool,    # Bắt buộc: ép dùng hàng đợi kết nối
    "pool_size": 5,            # Tối đa 5 kết nối
    "max_overflow": 0,         # Không cho phép kết nối dự phòng
    "pool_timeout": 0.02       # Timeout 20ms (nhỏ hơn p95=55ms) (ép kịch bản lý thuyết)
    }
    ```
    + *Tiến hành đo:* Chạy Kịch bản C, lưu bản báo cáo mới
    ```bash
    locust -f performance/locustfile.py --headless -H http://127.0.0.1:5000 -u 200 -r 50 -t 30s --html reports/pool_error.html
    ```
    + *Dấu hiệu nhận biết trong báo cáo Locust:*
        + Failure rate trên các endpoint truy vấn DB sẽ tăng vọt (> 40 - 60%).
        + Trong tab Failures sẽ xuất hiện lỗi `HTTP 500`.

- Kết quả kiểm thử xác nhận:

![pool_error](https://github.com/user-attachments/assets/e77d45b9-8afe-4794-97f0-ec8d7799e32e)

*Hình 1: Failures Statistics*

- Quan sát:
+ Đã xuất hiện nhiều lỗi HTTP 500 thực trên các endpoint truy vấn database.
+ Failure rate tăng vọt lên `3.42`.

> Không điền số liệu giả định vào bảng. Không khẳng định hiệu năng production
> từ SQLite + Flask development server trên máy cá nhân.
