@echo off
pushd "%~dp0"
python check_python.py
if %errorlevel% neq 0 exit /b %errorlevel%
pip install -r requirements.txt
mkdir config
pushd config
type nul > new.txt
type nul > quit.txt
type nul > watching.txt
echo {} > config.json
popd
popd