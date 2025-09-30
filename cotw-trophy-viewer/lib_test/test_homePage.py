from io import BytesIO

from fastapi import UploadFile
from nicegui import ui
from nicegui.testing import User

from lib.homePage import homePage
from lib.ui.utils.paths import Paths
from lib_test.fixtures import FIXTURES_PATH

pytest_plugins = ['nicegui.testing.user_plugin']


async def test_click(user: User) -> None:
    homePage(Paths(FIXTURES_PATH))
    await user.open('/')


async def test_upload_lodge(user: User) -> None:
    homePage(Paths(FIXTURES_PATH))
    await user.open('/')

    upload = user.find(ui.upload).elements.pop()
    lodge_file_path = FIXTURES_PATH / "trophy_lodges_adf"
    with open(lodge_file_path, 'rb') as f:
        io = BytesIO(f.read())
    upload.handle_uploads([UploadFile(
        io,
        filename='trophy_lodges_adf',
    )])

    user.find('RELOAD').click()
    # user.find('lodge').click()
    # user.find('1').click() # works in ui, issue with loading here?