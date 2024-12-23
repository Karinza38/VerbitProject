from playwright.sync_api import Page, expect, sync_playwright
from E2EAutomation.src.pages.DashboardPage import DashboardPage


class LoginPage:
    """
        A page object representing the login page of a web application (e.g., GitHub).

        This class encapsulates the functionality required to interact with the login form,
        such as entering a username and password, clicking the login button, and handling
        error messages and sign-out actions.

        Attributes:
            page (Page): The Playwright Page object representing the browser page.
            _username (Locator): Locator for the username input field.
            _pw (Locator): Locator for the password input field.
            _login_btn (Locator): Locator for the login button.
            _error_message (Locator): Locator for the error message displayed upon login failure.
            _sign_out_confirmation (Locator): Locator for the sign-out confirmation button.
    """
    def __init__(self, page):
        """
               Initializes the LoginPage with the given Playwright Page object.

               Args:
                   page (Page): The Playwright Page object representing the current browser page.
        """
        self.page = page
        self._username = page.locator("#login_field")
        self._pw = page.locator("#password")
        self._login_btn = page.locator("[name='commit']")
        self._error_message = page.locator("div[role='alert']")
        self._sign_out_confirmation = page.locator("input[value='Sign out from all accounts']")

    def enter_username(self, u_name):
        """
                Enters the provided username into the username field.

                Args:
                    u_name (str): The username to be entered into the login form.
        """
        self._username.clear()
        self._username.fill(u_name)

    def enter_password(self, pw):
        """
                Enters the provided password into the password field.

                Args:
                    pw (str): The password to be entered into the login form.
        """
        self._pw.clear()
        self._pw.fill(pw)

    def click_login(self):
        """
               Clicks the login button to submit the login form.

               This method simulates clicking the login button to attempt to log in.
        """
        self._login_btn.click()

    def do_login(self, credentials):
        """
                Performs the login action using the provided credentials.

                This method enters the username and password, clicks the login button,
                and returns an instance of the DashboardPage if login is successful.

                Args:
                    credentials (dict): A dictionary containing the 'username' and 'password'
                                         for logging into the application.

                Returns:
                    DashboardPage: The dashboard page object if login is successful.
        """
        self.enter_username(credentials['username'])
        self.enter_password(credentials['password'])
        self.click_login()
        return DashboardPage(self.page)

    @property
    def err_msg_loc(self):
        """
                Locator for the error message that appears when login fails.

                Returns:
                    Locator: The Playwright locator for the error message element.
        """
        return self._error_message

    @property
    def sign_out_confirmation_loc(self):
        """
                Locator for the sign-out confirmation button.

                Returns:
                    Locator: The Playwright locator for the sign-out confirmation button.
        """
        return self._sign_out_confirmation

