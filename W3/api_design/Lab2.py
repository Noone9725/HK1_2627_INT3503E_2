import logging
from flask import Flask, request, jsonify, make_response
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
# Thiết lập logging để ghi nhận lỗi phía server
logging.basicConfig(level=logging.ERROR)

# 1. Định nghĩa Exception class theo chuẩn RFC 7807 (Problem Details)
class ProblemError(Exception):
    def __init__(self, status, title, detail, type_uri="about:blank", instance=None):
        self.status = status
        self.title = title
        self.detail = detail
        self.type_uri = type_uri
        self.instance = instance

# 2. Handler cho các lỗi nghiệp vụ chủ động ném ra qua ProblemError
@app.errorhandler(ProblemError)
def handle_problem_error(error):
    response = {
        "type": error.type_uri,
        "title": error.title,
        "detail": error.detail,
        "status": error.status,
        "instance": error.instance or request.path
    }
    return make_response(jsonify(response), error.status, {'Content-Type': 'application/problem+json'})

# 3. Handler fallback cho các lỗi HTTP mặc định của Flask (ví dụ: 404, 405)
@app.errorhandler(HTTPException)
def handle_http_exception(error):
    response = {
        "type": "about:blank",
        "title": error.name,
        "detail": error.description,
        "status": error.code,
        "instance": request.path
    }
    return make_response(jsonify(response), error.code, {'Content-Type': 'application/problem+json'})

# 4. Handler cho các exception chưa được bắt (Lỗi 500)
@app.errorhandler(Exception)
def handle_unhandled_exception(error):
    # Ghi log chi tiết (bao gồm stack trace) ở phía server
    app.logger.error(f"Unhandled Exception: {error}", exc_info=True)
    
    # Trả về thông báo trung tính cho client, che giấu stack trace
    response = {
        "type": "about:blank",
        "title": "Internal Server Error",
        "detail": "Đã xảy ra lỗi hệ thống không mong muốn. Vui lòng thử lại sau.",
        "status": 500,
        "instance": request.path
    }
    return make_response(jsonify(response), 500, {'Content-Type': 'application/problem+json'})

# --- Các route giả lập để kiểm thử ---

# Route giả lập để test lỗi ProblemError
@app.route('/api/v1/trigger-problem', methods=['GET'])
def trigger_problem():
    raise ProblemError(
        status=400,
        title="Bad Request",
        detail="Thiếu trường dữ liệu bắt buộc.",
        type_uri="https://example.com/probs/missing-field"
    )

# Route giả lập để test lỗi hệ thống chưa bắt (chia cho 0)
@app.route('/api/v1/trigger-500', methods=['GET'])
def trigger_500():
    return 1 / 0

if __name__ == '__main__':
    app.run(debug=True, port=5000)