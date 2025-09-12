from nicegui.testing import User

from lib.ui.homePage import homePage

pytest_plugins = ['nicegui.testing.user_plugin']

async def test_click(user: User) -> None:
    homePage()
    await user.open('/')
    await user.should_see('FILTER')
    await user.should_see('UPLOAD LODGE')
    await user.should_see('RESET LODGE')
