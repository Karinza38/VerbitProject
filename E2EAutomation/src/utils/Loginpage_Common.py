import logging
from playwright.sync_api import Page, expect, sync_playwright

# Logger Configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig()

