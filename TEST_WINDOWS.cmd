@echo off
setlocal
cd /d "%~dp0"
echo ====================================================
echo CAPSTONE 1 - Windows verification
 echo ====================================================
where py >nul 2>&1
if not errorlevel 1 goto test_py
where python >nul 2>&1
if not errorlevel 1 goto test_python
echo ERROR: Python not found. Install Python 3.10+ and retry.
pause
exit /b 1
:test_py
py -3 -m unittest discover -v
set "TEST_EXIT=%errorlevel%"
goto finish
:test_python
python -m unittest discover -v
set "TEST_EXIT=%errorlevel%"
:finish
echo.
if "%TEST_EXIT%"=="0" (
  echo SUCCESS: All unit and integration tests passed.
) else (
  echo FAILED: One or more tests failed. Do not publish until fixed.
)
pause
exit /b %TEST_EXIT%
