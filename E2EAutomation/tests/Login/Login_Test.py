import pytest
from playwright.sync_api import Page, expect, sync_playwright

from E2EAutomation.src.pages.DashboardPage import DashboardPage
from E2EAutomation.src.pages.LoginPage import LoginPage


@pytest.mark.parametrize(
    "user, pw",
    [("danielbh2003@gmail.com", "sarit2608!")])
def test_login_with_private_user(set_up_tear_down, login_user, user, pw) -> None:
    """
    Test Case: Verify login functionality for a private user.

    Description:
    This test verifies that a private user can successfully log in to the application.
    After logging in, it checks that the dashboard page is displayed with the correct header.

    Parameters:
    - set_up_tear_down: Fixture to set up and tear down the test environment.
    - user (str): The username (email) of the private user.
    - pw (str): The password of the private user.

    Steps:
    1. Set up credentials using the provided username and password.
    2. Perform login using the LoginPage object.
    3. Verify that the dashboard header is visible.
    4. Confirm that the header text matches 'Dashboard'.

    Assertions:
    - Dashboard header is visible after login.
    - Dashboard header text is 'Dashboard'.
    """
    # Prepare credentials
    credentials = {'username' : user, 'password' : pw}

    # Setup
    dashboard_p = login_user(credentials)

    # Assertions
    expect(dashboard_p.product_header).to_be_visible()
    expect(dashboard_p.product_header).to_have_text("Dashboard")

@pytest.mark.parametrize(
    "user, pw",
    [("danielbh@gmail.com", "sarit2608!")])
def test_login_with_invalid_user(set_up_tear_down, login_user, user, pw) -> None:
    """
    Test Case: Verify login functionality with invalid credentials.

    Description:
    This test verifies that the application displays an error message when attempting to log in with invalid credentials.

    Parameters:
    - set_up_tear_down: Fixture to set up and tear down the test environment.
    - user (str): The invalid username (email) to be tested.
    - pw (str): The invalid password associated with the username.

    Steps:
    1. Prepare invalid credentials.
    2. Attempt login using the LoginPage object.
    3. Verify that an appropriate error message is displayed.

    Assertions:
    - Error message should contain the text 'Incorrect username or password'.
    """
    # Prepare credentials
    credentials = {'username': user, 'password': pw}

    # Setup
    page = set_up_tear_down
    login_p = LoginPage(page)
    login_p.do_login(credentials)

    er_ms = "Incorrect username or password"

    # Assertions
    expect(login_p.err_msg_loc).to_contain_text(er_ms)

def test_login_with_no_user(set_up_tear_down) -> None:
    """
    Test Case: Verify login behavior when no credentials are provided.

    Description:
    This test verifies that attempting to log in without entering any username or password does not grant access to the dashboard page.

    Parameters:
    - set_up_tear_down: Fixture to set up and tear down the test environment.

    Steps:
    1. Attempt to log in without entering any credentials.
    2. Verify that the dashboard header is not visible, indicating the user is not logged in.

    Assertions:
    - Dashboard header should not be visible after attempting login without credentials.
    """
    # setup
    page = set_up_tear_down
    login_p = LoginPage(page)

    # Attempt login without entering credentials
    login_p.click_login()
    # Create an instance of DashboardPage
    dashboard_p = DashboardPage(page)

    # Verify the dashboard header is NOT visible
    expect(dashboard_p.product_header).not_to_be_visible()

