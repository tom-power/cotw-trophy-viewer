@echo off
call .venv\Scripts\activate.bat
cd cotw-trophy-viewer
python -m PyInstaller mainNative.py ^
    --name cotwTrophyViewer.exe ^
    --onefile ^
    --noconsole ^
    --specpath .\build