@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 goto run_py
where python >nul 2>&1
if not errorlevel 1 goto run_python
echo Python 3.10 or newer is required. Install it and retry.
pause
exit /b 1
:run_py
py -3 launch.py
goto after
:run_python
python launch.py
:after
if errorlevel 1 (
    echo Application failed to start. See error above.
    pause
)
