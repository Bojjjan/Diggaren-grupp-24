@echo off


REM Get the directory where the script resides
set "os_dir=%~dp0"
cd "%os_dir%"

REM Define the script directory path relative to os_dir
set "script_dir=%os_dir%src\main\server\start_server.py"


REM Run the Python script with os_dir as an argument
python "%script_dir%" %os_dir%
pause