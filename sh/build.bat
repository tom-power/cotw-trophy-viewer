@echo off
call .venv\Scripts\activate.bat
cd cotw-trophy-viewer
rmdir /s /q build
rmdir /s /q dist
nicegui-pack --onefile --windowed --name "cotwTrophyViewer.exe" mainNative.py