# Script PowerShell để chạy Locust cho lab04

# Tạo thư mục reports nếu chưa tồn tại
if (-not (Test-Path -Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

Write-Host ">>> Kịch bản A: Baseline (10 users, 30s)..." -ForegroundColor Cyan
.venv\Scripts\locust.exe -f performance/locustfile.py --headless -H http://127.0.0.1:5000 -u 10 -r 2 -t 30s --html reports/A.html

Write-Host ">>> Kịch bản B: Load test thông thường (50 users, 60s)..." -ForegroundColor Cyan
.venv\Scripts\locust.exe -f performance/locustfile.py --headless -H http://127.0.0.1:5000 -u 50 -r 5 -t 60s --html reports/B.html

Write-Host ">>> Kịch bản C: Spike test (200 users, 30s)..." -ForegroundColor Cyan
.venv\Scripts\locust.exe -f performance/locustfile.py --headless -H http://127.0.0.1:5000 -u 200 -r 50 -t 30s --html reports/C.html

Write-Host ">>> Hoàn tất 3 kịch bản. Xem kết quả tại reports/A.html, reports/B.html, reports/C.html" -ForegroundColor Green