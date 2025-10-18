from typing import Callable

import watchfiles

from nicegui import ui
from lib.load.loader import Loader


class AutoReload:
    def __init__(self, loader: Loader, reloadFromLodgeFile: Callable):
        self._loader = loader
        self._reloadFromLodgeFile = reloadFromLodgeFile
        self._isAutoReload = False
        self._start()

    def _start(self):
        if self._loader.loadFileExists():
            ui.timer(0, self._auto_reload, once=True)

    async def _auto_reload(self):
        async for _ in watchfiles.awatch(str(self._loader.paths.getLoadPath().resolve())):
            if self._isAutoReload:
                self._reloadFromLodgeFile()

    def updateAutoReload(self, e):
        self._isAutoReload = e.value