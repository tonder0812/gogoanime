@echo off
pushd "%~dp0"
pip install -r requirements.txt
mkdir config
pushd config
type nul > new.txt
type nul > quit.txt
type nul > watching.txt
echo {} > config.json
popd
popd