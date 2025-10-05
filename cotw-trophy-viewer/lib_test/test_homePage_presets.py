from nicegui import ui
from nicegui.testing import User

from lib.model.medal import Medal
from lib.ui.utils.paths import Paths
from lib_test.fixtures import FIXTURES_PATH, getHomePage

pytest_plugins = ['nicegui.testing.user_plugin']

async def test_great_one_todo_preset(user: User) -> None:
    getHomePage(Paths(FIXTURES_PATH / 'trophy_lodges_adf'))
    await user.open('/')

    user.find('presets').click()
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
