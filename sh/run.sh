# Set the SQLite database path environment variable
. $PWD/sh/.env
source .venv/bin/activate &&
cd ./cotw-trophy-viewer && python3 ./__main__.py "$@"
