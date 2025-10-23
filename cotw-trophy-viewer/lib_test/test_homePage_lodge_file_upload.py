from io import BytesIO

from fastapi import UploadFile
from nicegui import ui
from nicegui.testing import User

from lib.ui.utils.paths import Paths
from lib_test.fixtures import FIXTURES_PATH, getHomePage
from lib_test.test_homePage_lodge_file import _has_layton_lake_option

pytest_plugins = ['nicegui.testing.user_plugin']

async def test_upload_lodge_file(user: User) -> None:
    getHomePage(paths=Paths(FIXTURES_PATH / 'no_file'))
    await user.open('/')

    await user.should_see('LODGE FILE NOT FOUND')
    assert not _has_layton_lake_option(user.find(ui.select).elements)

    upload = user.find(ui.upload).elements.pop()
    lodge_file_path = FIXTURES_PATH / 'trophy_lodges_adf'

    with open(lodge_file_path, 'rb') as f:
        upload.handle_uploads(
            [
                UploadFile(
                    file=(BytesIO(f.read())),
                    filename='trophy_lodges_adf'
                )
            ]
        )

    assert _has_layton_lake_option(user.find(ui.select).elements)




