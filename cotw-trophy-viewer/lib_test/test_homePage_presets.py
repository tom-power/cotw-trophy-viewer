from nicegui import ui
from nicegui.testing import User

from lib.model.medal import Medal
from lib.ui.utils.paths import Paths
from lib_test.fixtures import FIXTURES_PATH, getHomePage

pytest_plugins = ['nicegui.testing.user_plugin']

async def test_great_one_todo_preset_works(user: User) -> None:
    getHomePage(Paths(FIXTURES_PATH / 'trophy_lodges_adf'))
    await user.open('/')

    user.find('preset').click()
    user.find('great one todo').click()

    all_animals_checkbox = list(user.find(ui.checkbox).elements)[0]
    medal_select = None
    all_selects = user.find(ui.select).elements
    for select in all_selects:
        if hasattr(select, 'options') and isinstance(select.options, dict):
            if any(str(v).upper() in ['DIAMOND', 'GOLD', 'SILVER', 'BRONZE', 'GREAT_ONE'] for v in select.options.values()):
                medal_select = select
                break

    assert all_animals_checkbox.value is True
    assert Medal(Medal.GREAT_ONE).value == medal_select.value[0]

async def test_lodge_from_preset_works(user: User) -> None:
    getHomePage(Paths(FIXTURES_PATH / 'trophy_lodges_adf'))
    await user.open('/')

    user.find('preset').click()
    user.find('layton lake lodge todo').click()

    lodge_select = None
    all_selects = user.find(ui.select).elements
    for select in all_selects:
        if hasattr(select, 'options') and isinstance(select.options, dict):
            if any(str(v).upper() in ['LAYTON LAKE #1'] for v in select.options.values()):
                lodge_select = select
                break

    assert 1 == lodge_select.value[0]

async def test_lodge_from_preset_works_and_stays_selected(user: User) -> None:
    getHomePage(Paths(FIXTURES_PATH / 'trophy_lodges_adf'))
    await user.open('/')

    user.find('preset').click()
    user.find('layton lake lodge todo').click()

    lodge_select = None
    all_selects = user.find(ui.select).elements
    for select in all_selects:
        if hasattr(select, 'options') and isinstance(select.options, dict):
            if any(str(v).upper() in ['LAYTON LAKE #1'] for v in select.options.values()):
                lodge_select = select
                break

    assert 1 == lodge_select.value[0]

    user.find('RELOAD').click()

    assert 1 == lodge_select.value[0]
