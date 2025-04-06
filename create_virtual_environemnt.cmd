@echo off

REM Create a Python virtual environment named 'venv'
python -m venv venv
echo Virtual environment 'venv' has been created.

REM Activate the virtual environment
call venv\Scripts\activate.bat
echo Virtual environment 'venv' has been activated.

REM Install required packages
pip install -r requirements.txt
echo Required packages have been installed.
