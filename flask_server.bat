@echo off
REM === Set your project folder path here ===
cd /d "C:\Users\Administrator\Desktop\volunteersAI"

REM === Activate the virtual environment ===
call activate.bat

REM === Run your Flask app ===
python app.py

REM === Keep window open in case of errors ===
pause
