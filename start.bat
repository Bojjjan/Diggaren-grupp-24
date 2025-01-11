@echo off
setlocal

REM Set the current directory to the script's location
cd /d "%~dp0"

REM Define the script directory path relative to the current directory
set "script_dir=src\main\server\start_server.py"

REM Check if Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo  Python is not installed or not in your system's PATH environment variable.
    exit /b 1
)

REM Run the Python script with the current directory as an argument
python "%script_dir%" "%cd%"

endlocal
pause