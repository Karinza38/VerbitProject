import logging

from playwright.sync_api import Page

class IssueTabComponent:
    def __init__(self, page):
        self.page = page
        self._new_issue_btn = page.locator("//span[contains(text(), 'New issue')]")
        self._search_box = page.locator("input[data-testid='filter-input']")
        self._issue_list = page.locator("ul[data-listview-component='items-list']")
        self._close_issue_btn = page.locator("//span[contains(text(), 'Close issue')]")
        self._close_btn_status = page.locator("//*/react-app/div/div/div/div/div[2]/div/div/div/div/span")

    dict = {"open": "open", "closed": "closed"}

    @property
    def close_issue_btn_loc(self):
        return self._close_btn_status

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

    def select_ul_element(self, target_text: str):
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
            logging.info(f"Selecting '{target_text}' - Select <ul>/<ol> element by text.")

            # Locate the <ul> or <ol> element
            ul_element = self._issue_list
            #ul_element = self.page.locator("ul[data-listview-component='items-list']")

            # Find all <li> elements inside the specified <ul>
            li_elements = ul_element.locator("li")

            # Get the count of <li> elements
            count = li_elements.count()

            # Check if the <li> with the text exists
            for i in range(count):
                # Get the text content of each <li>
                li_text = li_elements.nth(i).inner_text().strip()

                # Check if the target text is in the <li> text
                if target_text.lower() in li_text.lower():
                    logging.info(f"Match found: {li_text}")

                    # Click the matched element
                    locator_string = "ul[data-listview-component='items-list'] li h3 span"
                    self.page.locator(locator_string).click()
                    return self

            # Raise error if no match is found
            raise ValueError(f"No <li> element found with text: '{target_text}'")

        except TimeoutError as e:
            logging.ERROR(f"Timeout error: {str(e)}")
            raise

    def click_close_issue_btn(self):
        """
        Clicks the 'New issue' button.
        """
        self._close_issue_btn.click()
