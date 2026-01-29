"""Edit BVN Page Object"""
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from utils.constants import EDIT_BVN_PAGE
from utils.decorators import log_method

logger = logging.getLogger(__name__)


class EditBvnPage(BasePage):
    """Page Object for Edit BVN."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        logger.info("🏗️ Initialized EditBvnPage")

    @log_method
    def enter_bvn(self, bvn: str) -> None:
        logger.info(f"🆔 Entering BVN")
        self.fill_input(EDIT_BVN_PAGE.EDIT_INPUT, bvn)

    @log_method
    def click_save_changes_button(self) -> None:
        self.click_element_by_text("Save Changes")
