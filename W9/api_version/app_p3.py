from datetime import datetime, timezone
import logging
from flask import Flask
from sunset import deprecate_at

logging.basicConfig(level=logging.WARNING)
app = Flask(__name__)

# Mốc thời gian tương lai (chưa hết hạn)
V1_SUNSET = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
# Mốc thời gian quá khứ (đã hết hạn) để test trực tiếp 410 Gone
V0_SUNSET = datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

@app.route("/api/v1/users/<int:uid>")
@deprecate_at(V1_SUNSET, replacement="/api/v2/users")
def get_v1(uid):
    return {"id": uid, "full_name": "Nguyễn Văn A"}

@app.route("/api/v0/users/<int:uid>")
@deprecate_at(V0_SUNSET, replacement="/api/v2/users")
def get_v0(uid):
    return {"id": uid, "full_name": "Nguyễn Văn A"}

if __name__ == "__main__":
    app.run(port=5000, debug=True)