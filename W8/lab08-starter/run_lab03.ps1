# Script PowerShell để chạy Newman với báo cáo JUnit XML cho lab03

# Tạo thư mục lưu kết quả nếu chưa có
if (-not (Test-Path -Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Chạy Newman với CLI output và xuất báo cáo JUnit XML
npx newman run books-api.postman_collection.json `
  -e postman/local.postman_environment.json `
  --reporters="cli,junit" `
  --reporter-junit-export reports/junit.xml