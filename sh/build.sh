source .venv/bin/activate &&
cd ./cotw-trophy-viewer &&
rm -rf ./build &&
rm -rf ./dist &&
nicegui-pack --onefile --windowed --name "cotwTrophyViewer" mainNative.py