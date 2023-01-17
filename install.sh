#!/bin/bash
pushd "$(dirname "$0")"
pip3 install -r requirements.txt
mkdir config
pushd config
touch new.txt
touch quit.txt
touch watching.txt
echo {} > config.json
popd
popd