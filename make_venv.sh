#!/usr/bin/env bash

set -e

python3 -m venv venv

source venv/bin/activate
pip install --upgrade pip
pip install pyyaml ninja

ln -sr build_setup.py venv/bin/build_setup.py
