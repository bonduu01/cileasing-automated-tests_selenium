"""Edit Emergency Contact Page Object"""
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from utils.constants import EDIT_EMERGENCY_CONTACT_PAGE
from utils.decorators import log_method

logger = logging.getLogger(__name__)


class EditEmergencyContactPage(BasePage):
    """Page Object for Edit Emergency Contact."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        logger.info("🏗️ Initialized EditEmergencyContactPage")

    @log_method
    def enter_first_name(self, first_name: str) -> None:
        self.fill_input(EDIT_EMERGENCY_CONTACT_PAGE.FIRST_NAME, first_name)

    @log_method
    def enter_mobile_number(self, mobile: str) -> None:
        self.fill_input(EDIT_EMERGENCY_CONTACT_PAGE.MOBILE_NUMBER, mobile)

    @log_method
    def click_save_changes_button(self) -> None:
        self.click_element_by_text("Save Changes")
