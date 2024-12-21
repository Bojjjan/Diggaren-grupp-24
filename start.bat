@echo off

set os_dir=%~dp0
set script_dir=%os_dir%src\main\server

python "%script_dir%\start_server.py" %os_dir%