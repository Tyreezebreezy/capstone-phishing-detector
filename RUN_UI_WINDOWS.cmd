@echo off
setlocal
cd /d "%~dp0"
echo CAPSTONE 1 - Local Phishing Detector
 echo When you see the address below, open http://127.0.0.1:8765 in your browser.
echo Press Ctrl+C to stop the server.
where py >nul 2>&1
if not errorlevel 1 goto run_py
where python >nul 2>&1
if not errorlevel 1 goto run_python
echo ERROR: Python not found. Install Python 3.10+ and retry.
pause
exit /b 1
:run_py
py -3 ui_server.py
goto after
:run_python
python ui_server.py
:after
if errorlevel 1 (
  echo Server failed to start. Check Python and whether port 8765 is in use.
  pause
)
