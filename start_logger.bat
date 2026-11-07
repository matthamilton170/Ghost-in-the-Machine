@echo off
cd /d C:\dev\Ghost-in-the-Machine
call .venv\Scripts\activate.bat
python src\tracker\listener.py
pause