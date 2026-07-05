@echo off
chcp 65001 >nul
cd /d %~dp0
echo [One Console AI] 의존성 확인...
py -m pip install -r server\requirements.txt --quiet --disable-pip-version-check
echo [One Console AI] 서버 시작: http://localhost:8000  (Swagger UI: /docs)
py -m uvicorn server.main:app --host 0.0.0.0 --port 8000
