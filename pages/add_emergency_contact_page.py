"""Add Emergency Contact Page Object"""
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from utils.constants import ADD_EMERGENCY_CONTACT_PAGE
from utils.decorators import log_method

logger = logging.getLogger(__name__)


class AddEmergencyContactPage(BasePage):
    """Page Object for Add Emergency Contact."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        logger.info("🏗️ Initialized AddEmergencyContactPage")

    @log_method
    def enter_first_name(self, first_name: str) -> None:
        self.fill_input(ADD_EMERGENCY_CONTACT_PAGE.FIRST_NAME, first_name)

    @log_method
    def enter_other_name(self, other_name: str) -> None:
        self.fill_input(ADD_EMERGENCY_CONTACT_PAGE.OTHER_NAME, other_name)

    @log_method
    def enter_surname(self, surname: str) -> None:
        self.fill_input(ADD_EMERGENCY_CONTACT_PAGE.SURNAME, surname)

    @log_method
    def enter_mobile_number(self, mobile: str) -> None:
        self.fill_input(ADD_EMERGENCY_CONTACT_PAGE.MOBILE_NUMBER, mobile)

    @log_method
    def enter_relationship(self, relationship: str) -> None:
        self.fill_input(ADD_EMERGENCY_CONTACT_PAGE.RELATIONSHIP, relationship)

    @log_method
    def click_add_contact_button(self) -> None:
        self.click_element_by_text("Add Contact")
