from nicegui.testing import User

from lib.ui.utils.paths import Paths
from lib_test.fixtures import FIXTURES_PATH, getHomePage
from lib_test.test_homePage import get_all_animals_checkbox_value, get_medal_select_value, get_presets_select_value

pytest_plugins = ['nicegui.testing.user_plugin']

async def test_clear_filter_works(user: User) -> None:
    getHomePage(Paths(FIXTURES_PATH / 'trophy_lodges_adf'))
    await user.open('/')

    user.find('preset').click()
    user.find('great one todo').click()

    assert get_all_animals_checkbox_value(user) is True
    assert get_medal_select_value(user) is not None
    assert get_presets_select_value(user) is not None

    user.find('CLEAR').click()

    assert get_all_animals_checkbox_value(user) is False
    assert get_medal_select_value(user) is None
    assert get_presets_select_value(user) is None

