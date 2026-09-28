# Homework W3

## I. Hoàn thiện Lab 3:

Sử dụng Composite Key để Sort ổn định tránh trường hợp sắp xếp theo trường có 2 giá trị trùng lặp.
Nếu giá trị trường bằng nhau, hệ thống tự động dùng `id` làm tiêu chí phụ (tie-breaker) để chốt cứng thứ tự bản ghi.

### SourceCodes:
[Lab3](/W3/api_design/Lab3.py)

### Kiểm thử:

- FirstPage:

![W3_L3_Sort](https://github.com/user-attachments/assets/e1acd99f-bebd-47e3-857a-77c00de75fcb)
*Hình 1: Test W3_L3_Sort*

- NextPage (NextCursor):

![W3_L3_Sort](https://github.com/user-attachments/assets/9c2026b5-7996-4247-bda5-41293e62f75a)
*Hình 1: Test W3_L3_Sort_Next_Page*

## II. Peer-Review GitHub REST API

**API đánh giá:** GitHub REST API (v3 / 2022-11-28)

### 1. Tài nguyên là danh từ
URLs chỉ chứa danh từ, không động từ. Method diễn đạt action. 

**Đạt:** Tài nguyên là danh từ. Sử dụng `/repos`, `/issues`, `/pulls`. Không chứa động từ hành động trong URL.

### 2. Naming nhất quán
Lowercase, kebab-case path; snake_case query; plurals cho collection.

**Đạt:** Naming nhất quán. Các path dùng lowercase, kebab-case (VD: `/search/code`), dùng số nhiều cho collection `/users`.

### 3. Status code đúng nghĩa
Mỗi response dùng code phù hợp. Không trả 200 + error trong body.

**Đạt:** Status code đúng nghĩa. Trả 201 Created khi tạo issue, 204 No Content khi xoá repository.

### 4. Idempotency rõ ràng
POST cần Idempotency-Key. PUT/DELETE idempotent. Tài liệu hoá rõ.

**Không đạt:** Idempotency rõ ràng. Thiếu tài liệu hoặc cơ chế bắt buộc dùng header Idempotency-Key cho đa số các thao tác POST.

POST không mang tính lũy đẳng (idempotent). Nếu client gọi API `POST /repos/{owner}/{repo}/issues` để tạo một issue mới nhưng gặp lỗi timeout mạng, client tự động retry sẽ vô tình tạo ra 2 issues giống hệt nhau do API không có cơ chế chặn trùng lặp qua key.

**Đề xuất sửa:** Yêu cầu client truyền thêm header `Idempotency-Key: <UUID>` vào mọi request `POST`. Server lưu key này lại trong thời gian ngắn. Nếu nhận được request POST có key trùng với giao dịch đã thành công, server trả về phản hồi lưu trong cache (kèm status 201 ban đầu) thay vì thực thi lại logic tạo mới tài nguyên trong database.

### 5. Error response có cấu trúc
RFC 7807 problem+json nhất quán. Có type, title, detail, instance.

**Không đạt:** Error response có cấu trúc. Không tuân thủ chuẩn RFC 7807 (problem+json). GitHub sử dụng cấu trúc lỗi tùy biến riêng (`{"message": "...", "documentation_url": "..."`}).

Khi gọi API sai, GitHub trả về Content-Type: application/json với body { "message": "Not Found", "documentation_url": "..." }. Điều này buộc client phải viết logic parse lỗi riêng cho GitHub thay vì dùng các thư viện xử lý lỗi RFC 7807 tiêu chuẩn.

**Đề xuất sửa:** Cập nhật endpoint để trả về `Content-Type: application/problem+json`. Chuyển đổi payload thành:
```json
{
  "type": "https://docs.github.com/rest/overview/resources-in-the-rest-api#not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "The requested repository does not exist.",
  "instance": "/repos/user/non-existent-repo"
}
```

### 6. Pagination rõ ràng
Collection nào cũng có phân trang (cursor/offset). Có giới hạn trên.

**Đạt:** Pagination rõ ràng. Hỗ trợ qua `page`, `per_page` kết hợp header `Link`. Có giới hạn `per_page` tối đa là 100.

### 7. Filter/Sort đa dạng
Hỗ trợ lọc theo field chính, sort đa field, sparse fieldsets.

**Đạt:** Filter/Sort đa dạng. Hỗ trợ query string mạnh (VD: `?sort=updated&direction=desc`).

### 8. Authentication & security
Token ở header. Không lộ qua URL. Rate limit rõ ràng.

**Đạt:** Authentication & security. Xác thực qua header `Authorization: Bearer <token>`. Rate limit được trả về rất rõ ràng trong các header `X-RateLimit-*`.

### 9. Versioning + deprecation
Có version prefix từ đầu. Có lộ trình ngừng hỗ trợ rõ ràng

**Đạt:** Versioning. Sử dụng header `X-GitHub-Api-Version` để ép versioning từ ngày đầu.

