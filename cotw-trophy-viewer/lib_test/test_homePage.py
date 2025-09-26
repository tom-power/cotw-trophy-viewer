from io import BytesIO

from fastapi import UploadFile
from nicegui import ui
from nicegui.testing import User

from lib.ui.homePage import homePage
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


async def test_diamond_checklist_preset(user: User) -> None:
    homePage(Paths(FIXTURES_PATH))
    await user.open('/')

    user.find('presets').click()
    user.find('diamond checklist').click()

    all_animals = list(user.find(ui.checkbox).elements)[0]
    assert all_animals.value is True

    medal_select = None
    all_selects = user.find(ui.select).elements
    for select in all_selects:
        if hasattr(select, 'options') and isinstance(select.options, dict):
            if any(str(v).upper() in ['DIAMOND', 'GOLD', 'SILVER', 'BRONZE'] for v in select.options.values()):
                medal_select = select
                break

    if medal_select:
        assert medal_select.value == [0], f"Expected medal selection [0] (Diamond), got {medal_select.value}"
    else:
        assert False, "Could not find medal select element"
