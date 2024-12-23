import time
import logging
from playwright.sync_api import sync_playwright

class BasePageObject:
    DEFAULT_TIMEOUT_MILLI = 60000
    PAGE_LOAD_TIMEOUT = 60  # seconds
    ELEMENT_LOAD_TIMEOUT = 30  # seconds

    def __init__(self, base_website, is_validate_page=True):
        """
        Initialize a BasePageObject with common page behavior.
        :param base_website: BaseWebSite object
        :param is_validate_page: Flag to validate page load (default is True)
        """
        self._base_website = base_website
        self._driver = base_website.driver
        self._base_url = base_website.env.get("BaseUrl")
        self.page_path = self.PagePath
        self.page_load_timeout = BasePageObject.PAGE_LOAD_TIMEOUT
        self.element_load_timeout = BasePageObject.ELEMENT_LOAD_TIMEOUT

        # Logging page load
        logging.debug(f"Load {self.page_path} page")

        # Validate page is loaded
        self.validate_page_is_loaded(is_validate_page)

    @property
    def PagePath(self):
        raise NotImplementedError("PagePath must be implemented in the child class.")

    @property
    def PageLoadMarker(self):
        raise NotImplementedError("PageLoadMarker must be implemented in the child class.")

    def open(self):
        """
        Navigate to the current page.
        """
        url = f"{self._base_url}/{self.page_path.lstrip('/')}"
        logging.debug(f"Navigate to '{url}'")
        self._driver.goto(url)

    def navigate(self, url):
        """
        Navigate to the provided full URL.
        :param url: The URL to navigate to
        """
        logging.debug(f"Navigate to '{url}'")
        self._driver.goto(url)

    def get_component(self, component, selector, refresh=False):
        """
        Initialize a component object.
        :param component: The component type (class)
        :param selector: The selector to locate the component
        :param refresh: Force refreshing the component (default=False)
        :return: The component object
        """
        if component is None or refresh:
            logging.debug(f"Creating component of type '{component.__name__}'")
            element = self._driver.query_selector(selector)
            component = component(element)
        return component

    def get_components(self, component, selector, refresh=False):
        """
        Get a list of initialized component objects.
        :param component: The component type (class)
        :param selector: The selector to locate the components
        :param refresh: Force refreshing the components (default=False)
        :return: List of component objects
        """
        components = []
        if refresh or not components:
            logging.debug(f"Creating list of components of type '{component.__name__}'")
            elements = self._driver.query_selector_all(selector)
            components = [component(e) for e in elements]
        logging.debug(f"Returning list size {len(components)} of components of type '{component.__name__}'")
        return components

    def validate_page_is_loaded(self, is_validate_page=True):
        """
        Validate that the page is loaded correctly.
        :param is_validate_page: Flag to validate page load (default is True)
        """
        if not is_validate_page:
            logging.info(f"Skipping validation for page {self.page_path}")
            return

        logging.info(f"Validating page load for '{self.page_path}'")

        # Wait for the page URL to contain the page path
        try:
            logging.debug(f"Validate page URL contains '{self.page_path}'")
            self._driver.wait_for_url(f"*{self.page_path}", timeout=self.page_load_timeout * 1000)
        except Exception:
            raise Exception(f"Expected page URL to contain '{self.page_path}', but got '{self._driver.url}'")

        # Validate document ready state is complete
        try:
            logging.debug("Validate document ready state is complete")
            self._driver.wait_for_selector("body", state="attached", timeout=self.page_load_timeout * 1000)
        except Exception:
            raise Exception("Document ready state is not complete!")

        # Validate page marker is visible
        try:
            logging.debug(f"Validate page marker '{self.PageLoadMarker}' is displayed")
            self._driver.wait_for_selector(self.PageLoadMarker, timeout=self.element_load_timeout * 1000)
        except Exception:
            raise Exception(f"Page marker '{self.PageLoadMarker}' was not displayed!")

        logging.info(f"Page '{self.page_path}' loaded successfully")

    def refresh(self, is_validate=True):
        """
        Refresh the current page and validate if needed.
        :param is_validate: If True, re-validate page load.
        """
        logging.info(f"Refreshing page '{self.page_path}'")
        self._driver.reload()
        self.validate_page_is_loaded(is_validate)


