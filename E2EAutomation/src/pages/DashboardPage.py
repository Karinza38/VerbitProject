from playwright.sync_api import Page, expect, sync_playwright

from E2EAutomation.src.Components.LeftPanelDashboard import LeftPanelDashboard
from E2EAutomation.src.pages.VSCodePage import VSCodePage


class DashboardPage:
    """
    DashboardPage class encapsulates actions and elements on the dashboard page.

    Attributes:
        page: The Playwright page instance.
        _dashboard_header: Locator for the dashboard header.
        _menu_btn: Locator for the profile menu button.
        _li_element_container: Locator for the list container within the profile menu.

    Methods:
        product_header: Returns the dashboard header element.
        click_menu_btn: Clicks the profile menu button to open the dropdown menu.
        click_sign_out: Selects the 'Sign out' option from the dropdown menu to log out.
    """
    def __init__(self, page):
        """
        Initializes the DashboardPage with required locators.

        Args:
            page: Playwright's Page object for interacting with the web page.
        """
        self.page = page
        self._dashboard_header = page.locator("span.AppHeader-context-item-label")
        self._menu_btn = page.locator("button.Button--invisible.Button--medium.Button.Button--invisible-noVisuals.color-bg-transparent.p-0")
        self._li_element_container = page.locator("ul.List__ListBox-sc-1x7olzq-0.eoXvfR")
        self.left_panel = LeftPanelDashboard(page)

    @property
    def product_header(self):
        """
        Returns:
            Locator: The dashboard header element.
        """
        return self._dashboard_header

    def click_menu_btn(self):
        """
        Clicks the profile menu button to open the dropdown menu.
        """
        self._menu_btn.click()

    def click_sign_out(self):
        """
        Clicks the 'Sign out' option in the dropdown menu to log out of the application.

        Iterates through all list items in the dropdown menu and clicks the one labeled 'Sign out'.
        """
        li_elements = self._li_element_container.locator("li").all()
        for li in li_elements:
            if li.inner_text().strip().lower() == "sign out":
                li.click()
                break

    def do_sign_out(self):
        """
            Signs out the current user by navigating to the sign-out option in the menu.

            This method simulates clicking on the menu button and then clicking the
            sign-out option to log out the user from the application.
        """
        self.click_menu_btn()  # Clicks the menu button to reveal options
        self.click_sign_out()  # Clicks the sign-out button to log out

    def get_btn_to_click(self, btn_name):
        return self.page.locator(f"div > loading-context > div > {btn_name} > div > ul > li > div > div > a")

    def click_ms_vscode_btn(self):
        self.left_panel.click_ms_vscode_btn()
        return VSCodePage(self.page)