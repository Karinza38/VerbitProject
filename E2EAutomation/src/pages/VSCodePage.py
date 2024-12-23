from playwright.sync_api import Page, expect, sync_playwright, Locator
from pytest_playwright.pytest_playwright import page

from E2EAutomation.src.Components.CreateNewIssueWindow import CreateNewIssueWindow
from E2EAutomation.src.Components.IssueTabComponent import IssueTabComponent
#from E2EAutomation.src.pages.DashboardPage import DashboardPage
from enum import Enum
from typing import Optional
import logging

class InnerTabs(Enum):
    CODE = "Code"
    ISSUES = "Issue"
    PULL_REQUESTS = "Pull Requests"
    ACTIONS = "Actions"
    PROJECTS = "Projects"
    WIKI = "Wiki"
    SECURITY = "Security"
    INSIGHTS = "Insights"

    @property
    def description(self) -> str:
        """
        Returns the description of the enum member.
        """
        return self.value

class VSCodePage:
    def __init__(self, page):
        self.page = page
        self._issue_tab = page.locator("#issues-tab")
        #self._issue_tab = page.locator(f"span[data-content='{InnerTabs.ISSUES.description}']")
        self._code_tab = page.locator(f"span[data-content='{InnerTabs.CODE.description}']")
        self._toolbar_locator = page.locator("ul.UnderlineNav-body.list-style-none")
        self.tab_path = ""
        self.tab_marker = None
        self.issue_tab_component = IssueTabComponent(page)
        self.create_new_issue_win = CreateNewIssueWindow(page)

        # Define locators for each tab
        self.tab_locators = {
            InnerTabs.CODE: "#code-tab",
            InnerTabs.ISSUES: "#issues-tab",
            InnerTabs.PULL_REQUESTS: "#pull-requests-tab",
            InnerTabs.ACTIONS: "#actions-tab",
            InnerTabs.PROJECTS: "#projects-tab",
            InnerTabs.WIKI: "#wiki-tab",
            InnerTabs.SECURITY: "#security-tab",
            InnerTabs.INSIGHTS: "#insights-tab"
        }

    @property
    def issue_tab_locator(self):
        """
        Returns:
            Locator: The dashboard header element.
        """
        return self._issue_tab

    @staticmethod
    def switch_to(toolbar_element: Locator, tab_locator: str) -> None:
        # Find the inner tab element within the toolbar
        inner_tab_element = toolbar_element.locator(tab_locator)
        logging.info(f"values: '{toolbar_element}': '{tab_locator}'")

        # Check if the tab is already clicked/selected based on its 'class' attribute
        if "selected" in inner_tab_element.get_attribute("class"):
            # Click the tab if it is not already selected
            inner_tab_element.click()
            logging.info(f"Switched to tab: '{tab_locator}'")
        else:
            # Log that the tab is already selected
            logging.debug(f"Already on '{tab_locator}' tab")

    def click_on_tab(self, tab_name: InnerTabs):
        """
        Clicks on the specified tab based on the tab name.
        Args:
            tab_name (str): The name of the tab to switch to.
        Returns:
            None
        """
        # Wait for toolbar to load
        toolbar_element = self._toolbar_locator
        toolbar_element.wait_for(state="visible")

        # waiting for jQuery completion
        self.page.wait_for_timeout(500)

        if tab_name == InnerTabs.CODE:
            self.switch_to(toolbar_element, self.tab_locators[InnerTabs.CODE])
            self.tab_path = "https://github.com/microsoft/vscode"
            self.tab_marker = f"{self.tab_locators[InnerTabs.CODE]}.clicked"
            raise NotImplementedError("SafetySelector is not yet implemented!")

        elif tab_name == InnerTabs.ISSUES:
            self.switch_to(toolbar_element, self.tab_locators[InnerTabs.ISSUES])
            self.tab_path = "https://github.com/microsoft/vscode/issues"
            self.tab_marker = f"{self.tab_locators[InnerTabs.ISSUES]}.clicked"

        else:
            raise NotImplementedError(f"Tab '{tab_name}' not implemented")

        logging.info(f"Successfully clicked on tab: {tab_name}")

    def click_new_issue_btn(self):
        self.issue_tab_component.click_new_issue_btn()
        return self

    def select_bug_report(self):
        self.create_new_issue_win.issue_popup(CreateNewIssueWindow.IssueOptions.BUG_REPORT)
        return self

    def add_title_and_description_and_create_issue(self, info):
        self.create_new_issue_win.add_title_and_description_and_create(info)
        return self