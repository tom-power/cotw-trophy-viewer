from nicegui.testing import User

from lib.ui.homePage import homePage
from lib.ui.utils.paths import Paths
from lib_test.fixtures import FIXTURES_PATH

pytest_plugins = ['nicegui.testing.user_plugin']

async def test_click(user: User) -> None:
    homePage(Paths(FIXTURES_PATH))
    await user.open('/')
    await user.should_see('FILTER')
    await user.should_see('UPLOAD LODGE')
    await user.should_see('RESET LODGE')
    await user.should_see('COTW SAVE FILE -> FOUND')
