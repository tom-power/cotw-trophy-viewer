from nicegui.testing import User

from lib.ui.homePage import homePage
from lib.ui.utils.paths import Paths
from lib_test.fixtures import FIXTURES_PATH

pytest_plugins = ['nicegui.testing.user_plugin']

async def test_click(user: User) -> None:
    homePage(Paths(FIXTURES_PATH))
    await user.open('/')
