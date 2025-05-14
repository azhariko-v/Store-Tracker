@echo off
echo Installing Store Management System as a Windows service...
echo.
echo This will make the application run automatically in the background
echo and be accessible at http://localhost:8080
echo.
echo Please run this script as Administrator!
echo.
pause

REM Install the service
python store_service.py install

echo.
echo Service installed. Starting service...
echo.

REM Start the service
python store_service.py start

echo.
echo Service started! You can now access your application at:
echo.
echo     http://localhost:8080
echo.
echo This service will start automatically when your computer boots.
echo.
echo To manage the service:
echo - Use Windows Services manager (services.msc)
echo - Or use the provided batch files (start_store.bat, stop_store.bat)
echo.
pause