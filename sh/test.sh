#!/bin/sh
source .venv/bin/activate &&
python3 -m pytest -vv ./cotw-trophy-viewer/lib_test/ --maxfail=1

