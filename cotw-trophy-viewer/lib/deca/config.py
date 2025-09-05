import os
import re
import sys
from pathlib import Path


APP_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))

def _find_saves_path() -> Path | None:
    steam_saves = Path().home() / "Documents/Avalanche Studios/COTW/Saves"
    steam_onedrive = Path().home() / "OneDrive/Documents/Avalanche Studios/COTW/Saves"
    epic_saves = Path().home() / "Documents/Avalanche Studios/Epic Games Store/COTW/Saves"
    epic_onedrive = Path().home() / "OneDrive/Documents/Avalanche Studios/Epic Games Store/COTW/Saves"

    base_saves = None
    if steam_saves.exists():
        base_saves = steam_saves
    elif epic_saves.exists():
        base_saves = epic_saves
    elif steam_onedrive.exists():
        base_saves = steam_onedrive
    elif epic_onedrive.exists():
        base_saves = epic_onedrive

    save_folder = None
    if base_saves:
        folders = os.listdir(base_saves)
        all_numbers = re.compile(r"\d+")
        for folder in folders:
            if all_numbers.match(folder):
                save_folder = folder
                break
    if save_folder:
        return base_saves / save_folder
    else:
        return None

DEFAULT_SAVE_PATH = _find_saves_path()

def get_save_path() -> Path:
  return DEFAULT_SAVE_PATH