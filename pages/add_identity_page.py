"""Add Identity Page Object"""
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from utils.constants import ADD_IDENTITY_PAGE
from utils.decorators import log_method

logger = logging.getLogger(__name__)


class AddIdentityPage(BasePage):
    """Page Object for Add Identity."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        logger.info("🏗️ Initialized AddIdentityPage")

    @log_method
    def select_identity_type(self, identity_type: str) -> None:
        logger.info(f"🪪 Selecting identity type: {identity_type}")
        self.ant_select_option(ADD_IDENTITY_PAGE.IDENTITY_TYPE_DROPDOWN, identity_type)

    @log_method
    def enter_identity_id(self, identity_id: str) -> None:
        logger.info(f"🆔 Entering identity ID")
        self.fill_input(ADD_IDENTITY_PAGE.IDENTITY_ID, identity_id)

    @log_method
    def enter_issued_date(self, date: str) -> None:
        logger.info(f"📅 Entering issued date")
        self.ant_select_date_picker(ADD_IDENTITY_PAGE.ISSUED_DATE_SELECTOR, date)

    @log_method
    def enter_expiry_date(self, date: str) -> None:
        logger.info(f"📅 Entering expiry date")
        self.ant_select_date_picker(ADD_IDENTITY_PAGE.EXPIRY_DATE_SELECTOR, date)

    @log_method
    def click_add_button(self) -> None:
        self.click_element_by_text("Add")
