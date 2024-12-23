from playwright.sync_api import Page
from playwright.sync_api import sync_playwright

class LeftPanelDashboard:
    """
    LeftPanel class encapsulates interactions with the left navigation panel,
    including the 'Microsoft/vscode' button.
    """

    def __init__(self, page):
        """
        Initializes the LeftPanel component with required locators.

        Args:
            page: Playwright's Page object for interacting with the web page.
        """
        self.page = page
        # Locator for the Microsoft/vscode button
        self._ms_vscode_btn = page.locator("body > div.logged-in.env-production.page-responsive.full-width > div.application-main > div > div > aside > div > div > loading-context > div > div.Details.js-repos-container.mt-5 > div > ul > li > div > div > a")

    def click_ms_vscode_btn(self):
        """
        Clicks the 'Microsoft/vscode' button in the left panel to navigate to the repository.
        """
        self._ms_vscode_btn.click()