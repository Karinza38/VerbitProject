import pytest
from playwright.sync_api import expect
from E2EAutomation.src.pages.LoginPage import LoginPage
from E2EAutomation.src.pages.DashboardPage import DashboardPage

@pytest.mark.parametrize(
    "user, pw",
    [("danielbh2003@gmail.com", "sarit2608!")])
def test_logout(set_up_tear_down, login_user, user, pw) -> None:
    """
    Test Case: Verify logout functionality for a logged-in user.

    Description:
    This test ensures that a user can successfully log out of the application.
    After logging in with valid credentials, the test clicks on the logout button,
    verifies that the logout option appears, and confirms that the sign-out page is displayed.

    Parameters:
    - set_up_tear_down: Fixture to set up and tear down the test environment.
    - user (str): The username (email) of the private user.
    - pw (str): The password of the private user.

    Steps:
    1. Log in with valid credentials.
    2. Click the logout button.
    3. Select the 'Sign Out' option.
    4. Verify that the sign-out confirmation page is displayed.

    Assertions:
    - Verify that the 'Sign out from all accounts' input button is enabled.
    """
    credentials = {'username': user, 'password': pw}

    # Setup
    page = set_up_tear_down
    login_p = LoginPage(page)
    dashboard_p = login_p.do_login(credentials)

    # Perform logout
    dashboard_p.do_sign_out()

    # Verify sign-out confirmation
    expect(login_p.sign_out_confirmation_loc).to_be_enabled()