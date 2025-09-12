import os
import subprocess
from pathlib import Path
import nicegui

cmd = [
    'python',
    '-m', 'PyInstaller',
    'mainNative.py', # your main file with ui.run()
    '--name', 'cotwTrophyViewer.exe', # name of your app
    '--onefile',
    '--noconsole', # prevent console appearing, only use with ui.run(native=True, ...)
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui',
    '--specpath', './build'
]
subprocess.call(cmd)