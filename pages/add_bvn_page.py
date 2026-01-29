"""Add BVN Page Object"""
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from utils.constants import ADD_BVN_PAGE
from utils.decorators import log_method

logger = logging.getLogger(__name__)


class AddBvnPage(BasePage):
    """Page Object for Add BVN."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        logger.info("🏗️ Initialized AddBvnPage")

    @log_method
    def enter_bvn(self, bvn: str) -> None:
        logger.info(f"🆔 Entering BVN")
        self.fill_input(ADD_BVN_PAGE.BVN_INPUT, bvn)

    @log_method
    def click_add_bvn_button(self) -> None:
        self.click_element_by_text("Add BVN")
