from nicegui import ui
from nicegui.testing import User

from lib.model.medal import Medal
from lib.ui.utils.paths import Paths
from lib_test.fixtures import FIXTURES_PATH, getHomePage
from lib_test.test_homePage import get_lodge_select_value, get_medal_select_value, get_all_animals_checkbox_value

pytest_plugins = ['nicegui.testing.user_plugin']

async def test_great_one_todo_preset_works(user: User) -> None:
    getHomePage(Paths(FIXTURES_PATH / 'trophy_lodges_adf'))
    await user.open('/')

    user.find('preset').click()
    user.find('great one todo').click()

    assert get_all_animals_checkbox_value(user) is True
    assert get_medal_select_value(user) == Medal(Medal.GREAT_ONE).value

async def test_lodge_from_preset_works(user: User) -> None:
    getHomePage(Paths(FIXTURES_PATH / 'trophy_lodges_adf'))
    await user.open('/')

    user.find('preset').click()
    user.find('layton lake lodge todo').click()

    assert get_lodge_select_value(user) == 1

async def test_lodge_from_preset_works_and_stays_selected(user: User) -> None:
    getHomePage(Paths(FIXTURES_PATH / 'trophy_lodges_adf'))
    await user.open('/')

    user.find('preset').click()
    user.find('layton lake lodge todo').click()

    assert get_lodge_select_value(user) == 1

    user.find('RELOAD').click()

    assert get_lodge_select_value(user) == 1
