@echo off
echo Creating desktop shortcut to Store Management System...

REM Get the current directory
set CURRENT_DIR=%~dp0

REM Create a shortcut on the desktop
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\Store Management System.url" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "http://localhost:8080" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript CreateShortcut.vbs
del CreateShortcut.vbs

echo.
echo Desktop shortcut created!
echo.
echo You can now access your application by clicking the shortcut on your desktop.
echo.
pause