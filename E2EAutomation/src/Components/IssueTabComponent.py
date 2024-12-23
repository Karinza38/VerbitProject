import logging

from playwright.sync_api import Page

class IssueTabComponent:
    def __init__(self, page):
        self.page = page
        self._new_issue_btn = page.locator("//span[contains(text(), 'New issue')]")
        self._search_box = page.locator("//*[@id='repository'']/div/div[1]/button")
        self._issue_list = page.locator("ul[data-listview-component='items-list']")

    def click_new_issue_btn(self):
        """
        Clicks the 'New issue' button.
        """
        self._new_issue_btn.click()

    def search_issue(self, query):
        """
        Searches for an issue based on the given query.

        Args:
            query (str): The search term to look for issues.
        """
        self._search_box.fill(query)
        self._search_box.press("Enter")

    def get_issue_titles(self):
        """
        Retrieves all issue titles from the list.

        Returns:
            list: A list of issue titles.
        """
        return [issue.inner_text() for issue in self._issue_list.locator("a.Link--primary").all()]

    def select_ul_element(self, ul_locator: str, text: str):
        """
        Selects a <li> element within a <ul> element by its visible text using Playwright.

        Args:
        - page (Page): Playwright Page instance.
        - ul_locator (str): Locator for the <ul> or <ol> element.
        - text (str): The text to match in the <li> elements.

        Raises:
        - ValueError: If no <li> element with the specified text is found.
        """

        try:
            # Log the action
            logging.info(f"Selecting '{text}' - Select <ul>/<ol> element by text.")

            # Locate the <ul> or <ol> element
            ul_element = self.page.locator("ul[data-listview-component='items-list']")

            # Find all <li> elements inside the specified <ul>
            li_elements = ul_element.locator("li")

            # Find the <li> element with the specified text
            li_element_to_select = li_elements.locator(f"text='{text}'")

            # Check if the <li> with the text exists
            if not li_element_to_select.count():
                logging.info(f"No <li> element with text '{text}' found.")
                raise ValueError(f"No <li> element with text '{text}' found.")

            # Click the <li> element
            li_element_to_select.first.click()
            logging.info(f"Clicked on <li> element with text '{text}'.")

        except TimeoutError as e:
            logging.ERROR(f"Timeout error: {str(e)}")
            raise
        except Exception as e:
            logging.ERROR(f"Error: {str(e)}")
            raise