#!/bin/bash
set -e

pushd "$(dirname "$0")"
python3 check_python.py
pip3 install -r requirements.txt
mkdir config
pushd config
touch new.txt
touch quit.txt
touch watching.txt
echo {} > config.json
popd
popd