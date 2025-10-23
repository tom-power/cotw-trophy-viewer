from io import BytesIO
from pathlib import Path

from fastapi import UploadFile
from nicegui import ui
from nicegui.testing import User

from lib.ui.utils.paths import Paths
from lib_test.fixtures import FIXTURES_PATH, getHomePage
from lib_test.test_homePage_lodge_file import _has_layton_lake_option

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

