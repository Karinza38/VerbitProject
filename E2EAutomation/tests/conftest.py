import pytest

from E2EAutomation.src.pages.LoginPage import LoginPage


@pytest.fixture()
def set_up_tear_down(page):
    """
    Fixture to set up the initial conditions for tests that require a login page.

    This fixture does the following:
    1. Sets the viewport size to 1536x800 for consistent rendering across tests.
    2. Navigates to the GitHub login page.

    After the test is executed, the fixture will automatically clean up (this can be
    expanded if needed with further teardown logic).

    Args:
        page: The page object provided by Playwright, representing the browser page.

    Yields:
        page: The same page object, ready for use in the test.
    """
    # Set the viewport size for consistent rendering
    page.set_viewport_size({"width": 1536, "height": 800})

    # Navigate to the GitHub login page
    page.goto("https://github.com/login")

    # Yield the page object to the test function
    yield page

@pytest.fixture()
def login_user(set_up_tear_down):
    # Initialize the page object
    page = set_up_tear_down
    login_p = LoginPage(page)

    def do_login(credentials):
        """
        Perform login and return an instance of the DashboardPage object after successful login.
        """
        dashboard_p = login_p.do_login(credentials)
        return dashboard_p
    # Returns: function: A callable function (`do_login`) that accepts credentials as input and performs login, returning the dashboard page object.
    return do_login