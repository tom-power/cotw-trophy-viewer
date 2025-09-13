@echo off
call .venv\Scripts\activate.bat
cd cotw-trophy-viewer
nicegui-pack --onefile --name "cotwTrophyViewer" mainNative.py