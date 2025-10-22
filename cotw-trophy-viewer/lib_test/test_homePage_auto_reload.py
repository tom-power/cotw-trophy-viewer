from io import BytesIO
from pathlib import Path

from fastapi import UploadFile
from nicegui import ui
from nicegui.testing import User

from lib.ui.utils.paths import Paths
from lib_test.fixtures import FIXTURES_PATH, getHomePage

pytest_plugins = ['nicegui.testing.user_plugin']


async def test_lodge_file_auto_reload(user: User) -> None:
    getHomePage(paths=Paths(FIXTURES_PATH / 'trophy_lodges_adf'))

    await user.open('/')

    await user.should_see('LODGE FILE FOUND')
    assert _has_layton_lake_option(user.find(ui.select).elements)

    user.find('lodge').click()
    user.find('LAYTON LAKE #1').click()
    await user.should_see('LAYTON LAKE #1')

    Paths(FIXTURES_PATH / 'trophy_lodges_adf').getLoadPath().touch()

    await user.should_see('LAYTON LAKE #1')

def _has_layton_lake_option(all_selects: set) -> bool:
    foundLaytonLake = False
    for select in all_selects:
        if hasattr(select, 'options') and isinstance(select.options, dict):
            # print(select.options.values())
            if 'LAYTON LAKE #1' in select.options.values():
                foundLaytonLake = True
    return foundLaytonLake


