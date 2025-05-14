@echo off
echo Starting Store Management Service...
python store_service.py start
echo.
echo Service started! You can now access your application at:
echo     http://localhost:8080
echo.
start "" http://localhost:8080
pause