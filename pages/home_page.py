"""
Home Page Object Model
"""
from selenium.webdriver.common.by import By

from config.settings import settings
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class HomePage(BasePage):

    def __init__(self, driver):
        """Initialize Home Page"""
        super().__init__(driver)
        self.url = settings.base_url
        logger.info(f"🏗️ Initialized HomePage - URL: {self.url}")

    def go_to_home_page(self) -> None:
        """Navigate to the home page."""
        logger.info(f"🔄 Navigating to home page: {self.url}")
        self.open_url(self.url)
