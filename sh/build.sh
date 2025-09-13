source .venv/bin/activate &&
cd ./cotw-trophy-viewer && 
python3 -m PyInstaller mainNative.py \
    --name cotwTrophyViewer.exe  \
    --onefile \
    --noconsole \
    --specpath ./build
