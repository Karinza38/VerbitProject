from playwright.sync_api import Page
from enum import Enum
import logging

class CreateNewIssueWindow:
    """
    A class for interacting with the 'Create New Issue' window in a VSCode-like environment.

    This class provides methods to interact with various fields and buttons in the 'Create New Issue' pop-up window.
    It supports setting issue types, adding titles, descriptions, and creating the issue.

    Attributes:
    ----------
    page : Page
        The Playwright page object used for interacting with the UI elements.

    IssueOptions : Enum
        An enumeration defining different issue types available in the pop-up window.
    """

    class IssueOptions(Enum):
        """
        Enum representing the available issue types in the 'Create New Issue' window.
        """
        BUG_REPORT = "Bug report"
        FEATURE_REQUEST = "Feature request"
        SECURITY_VULNERABILITY = "Report a security vulnerability"
        QUESTION = "Question"
        EXTENSION_DEVELOPMENT = "Extension Development"

    def __init__(self, page):
        self.page = page
        self._title_input = page.locator("input[placeholder='Title']")
        self._description_input = page.locator("textarea[placeholder='Type your description here…']")
        self._create_btn = page.locator("//span[contains(text(), 'Create')]")

    def issue_popup(self, option: IssueOptions):
        """
        Selects an issue type from the pop-up window.

        Parameters:
        ----------
        option : IssueOptions
        The type of issue to select from the available options.
        """
        locator = self.page.locator(f"//span[contains(text(), '{option.value}')]")
        locator.click()
        logging.info(f"Selected option: {option.value}")

    def add_title(self, title: str):
        """
        Adds a title to the new issue.

        Parameters:
        ----------
        title : str
        The title text to be added to the issue.
        """
        self._title_input.clear()
        self._title_input.fill(title)
        logging.info(f"Added title: {title}")

    def add_description(self, description: str):
        """
        Adds a description to the new issue.

        Parameters:
        ----------
        description : str
        The description text to be added to the issue.
        """
        self._description_input.clear()
        self._description_input.fill(description)
        logging.info(f"Added description: {description}")

    def click_create(self):
        """
        Clicks the 'Create' button to submit the issue.
        """
        self._create_btn.click()
        logging.info("Clicked 'Create' button.")

    def add_title_and_description_and_create(self, info):
        """
        Combine the add title, add description and click on create btn
        """
        self.add_title(info['title'])
        self.add_description(info['description'])
        self.click_create()
        logging.info(f"Added title: {info['title']}, Added description: info['description'] and clicked on create issue")



