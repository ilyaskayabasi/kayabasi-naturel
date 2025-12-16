@echo off
REM Django development server'ını static dosyalarla çalıştır
cd /d "%~dp0"
.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000 --insecure
pause
