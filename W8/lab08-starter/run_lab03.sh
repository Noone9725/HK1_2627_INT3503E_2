# Script Bash để chạy Newman với báo cáo JUnit XML cho lab03

#!/usr/bin/env bash
mkdir -p reports
newman run books-api.postman_collection.json \
  -e postman/local.postman_environment.json \
  -r cli,junit --reporter-junit-export reports/junit.xml