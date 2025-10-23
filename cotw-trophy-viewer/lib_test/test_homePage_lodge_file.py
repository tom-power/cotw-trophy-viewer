from io import BytesIO

from fastapi import UploadFile
from nicegui import ui
from nicegui.testing import User

from lib.ui.utils.paths import Paths
from lib_test.fixtures import FIXTURES_PATH, getHomePage

pytest_plugins = ['nicegui.testing.user_plugin']


async def test_lodge_file_found(user: User) -> None:
    getHomePage(paths=Paths(FIXTURES_PATH / 'trophy_lodges_adf'))

    await user.open('/')

    await user.should_see('LODGE FILE FOUND')
    assert _has_layton_lake_option(user.find(ui.select).elements)


async def test_lodge_file_not_found(user: User) -> None:
    getHomePage(paths=Paths(FIXTURES_PATH / 'no_file'))

    await user.open('/')

    await user.should_see('LODGE FILE NOT FOUND')
    assert not _has_layton_lake_option(user.find(ui.select).elements)

def _has_layton_lake_option(all_selects: set) -> bool:
    foundLaytonLake = False
    for select in all_selects:
        if hasattr(select, 'options') and isinstance(select.options, dict):
            # print(select.options.values())
            if 'LAYTON LAKE #1' in select.options.values():
                foundLaytonLake = True
    return foundLaytonLake


