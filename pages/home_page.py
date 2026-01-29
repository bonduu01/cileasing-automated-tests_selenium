"""
Home Page Object
"""

import logging
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from config import settings
from utils.constants import HOME_PAGE
from utils.decorators import log_method, log_page_state

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """Page Object for the Home Page."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.url = settings.base_url
        logger.info(f"🏗️ Initialized HomePage - URL: {self.url}")

    @log_method
    @log_page_state
    def go_to_home_page(self) -> None:
        """Navigate to the home page."""
        logger.info(f"🔄 Navigating to home page: {self.url}")
        self.navigate_to(self.url)

    @log_method
    def verify_home_page_loads(self) -> None:
        """Verify that the home page has loaded successfully."""
        logger.info(f"✅ Verifying home page loaded")
        self.verify_title_contains(HOME_PAGE.TITLE)
        logger.info(f"   ✅ Home page title verified: {self.driver.title}")
