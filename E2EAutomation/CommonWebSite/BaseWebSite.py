import logging
from playwright.sync_api import sync_playwright

from E2EAutomation.CommonWebSite.BaseEnv import BaseENV


class BaseWebSite:
    DEFAULT_TIMEOUT_MILLI = 60000

    def __init__(self, env, browser_instance=None):
        self.env = env
        self.driver = browser_instance
        self._initialize_driver()

    def _initialize_driver(self):
        if self.driver:
            return

        browser_type = self.env.get("EngineType")
        is_headless = self.env.get("IsHeadless", False)

        # Launch browser based on engine type
        with sync_playwright() as p:
            if browser_type == "Chrome":
                logging.info("Running Chrome browser" if not is_headless else "Running Chrome headless mode")
                self.driver = p.chromium.launch(headless=is_headless)

            elif browser_type == "Firefox":
                logging.info("Running Firefox browser" if not is_headless else "Running Firefox headless mode")
                self.driver = p.firefox.launch(headless=is_headless)

            elif browser_type == "WebKit":  # WebKit represents Safari in Playwright
                logging.info("Running WebKit browser" if not is_headless else "Running WebKit headless mode")
                self.driver = p.webkit.launch(headless=is_headless)

            else:
                logging.error(f"Browser type {browser_type} is not implemented")
                raise NotImplementedError(f"Browser type {browser_type} is not implemented")

            # Set window size for headless mode
            if is_headless:
                logging.debug(f"Running in Headless mode resolution: 1920x1080")
                self.context = self.driver.new_context(viewport={"width": 1920, "height": 1080})
            else:
                self.context = self.driver.new_context()

            self.page = self.context.new_page()

    def close_site(self):
        if self.driver:
            self.driver.close()

    def take_screenshot(self, file_name, description):
        if self.page:
            self.page.screenshot(path=file_name)
            logging.info(f"Screenshot taken: {description}")

    def open_page(self, url):
        logging.info(f"Open '{url}' page")
        self.page.goto(url)
        # Returning self to allow method chaining if needed
        return self



