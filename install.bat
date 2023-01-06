@echo off
mkdir config
pushd config
type nul > new.txt
type nul > quit.txt
type nul > watching.txt
echo {} > config.json
popd