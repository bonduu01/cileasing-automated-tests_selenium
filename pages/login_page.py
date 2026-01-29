"""
Login Page Object
"""

import logging
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.self_service_page import SelfServicePage
from config import settings
from utils.constants import LOGIN_PAGE
from utils.decorators import log_method, log_page_state

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Page Object for the Login Page."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.url = settings.base_url
        logger.info(f"🏗️ Initialized LoginPage - URL: {self.url}")

    @log_method
    @log_page_state
    def go_to_login_page(self) -> None:
        """Navigate to the login page."""
        logger.info(f"🔄 Navigating to login page: {self.url}")
        self.navigate_to(self.url)

    @log_method
    def login_user(self, email: str = None, password: str = None) -> None:
        """Perform login with provided or default credentials."""
        email = email or settings.test_username
        password = password or settings.test_password

        logger.info(f"🔐 Attempting login with email: {email}")

        self.fill_input(LOGIN_PAGE.EMAIL_INPUT, email)
        self.fill_input(LOGIN_PAGE.PASSWORD_INPUT, password)
        self.click_element(LOGIN_PAGE.SUBMIT_BUTTON)

        logger.info("✅ Login form submitted")

    @log_method
    def enter_email(self, email: str) -> None:
        """Enter email address."""
        logger.info(f"📧 Entering email: {email}")
        self.fill_input(LOGIN_PAGE.EMAIL_INPUT, email)

    @log_method
    def enter_password(self, password: str) -> None:
        """Enter password."""
        logger.info(f"🔑 Entering password: {'*' * len(password)}")
        self.fill_input(LOGIN_PAGE.PASSWORD_INPUT, password)

    @log_method
    def click_login_button(self) -> None:
        """Click the login button."""
        logger.info("🖱️ Clicking login button")
        self.click_element(LOGIN_PAGE.SUBMIT_BUTTON)

    @log_method
    def verify_login_successful_load_companies(self) -> None:
        """Assert that the login successful message is displayed."""
        logger.info("✅ Verifying successful login - checking for company list")
        # Verify DEFAULT company is visible
        self.verify_element_visible(LOGIN_PAGE.DEFAULT_COMPANY)
        # Verify text "DEFAULT" is present
        self.verify_text_visible("DEFAULT")
        logger.info("✅ Company list verified")

    @log_method
    def verify_error_message(self) -> None:
        """Assert an error message is displayed."""
        logger.info("⚠️ Verifying error message is displayed")
        self.verify_has_text_visible(LOGIN_PAGE.ERROR_TOAST, LOGIN_PAGE.ERROR_INVALID_CREDENTIALS)

    @log_method
    def verify_error_toast_visible(self) -> None:
        """Verify error toast alert is visible."""
        logger.info("🔍 Checking if error toast is visible")
        self.verify_element_visible(LOGIN_PAGE.ERROR_TOAST, timeout=5)

    @log_method
    def verify_password_blank_error(self) -> None:
        """Verify 'Password cannot be blank' validation error."""
        logger.info("🔍 Verifying password blank error")
        self.verify_validation_error(LOGIN_PAGE.ERROR_PASSWORD_BLANK)

    @log_method
    def verify_username_blank_error(self) -> None:
        """Verify 'Username cannot be blank' validation error."""
        logger.info("🔍 Verifying username and password blank errors")
        self.verify_validation_error(LOGIN_PAGE.ERROR_USERNAME_BLANK)
        self.verify_validation_error(LOGIN_PAGE.ERROR_PASSWORD_BLANK)

    @log_method
    def is_password_blank_error_visible(self) -> bool:
        """Check if password blank error is visible."""
        logger.info("👁️ Checking password blank error visibility")
        result = self.is_validation_error_visible(LOGIN_PAGE.ERROR_PASSWORD_BLANK)
        logger.info(f"   Result: {result}")
        return result

    @log_method
    def is_username_blank_error_visible(self) -> bool:
        """Check if username blank error is visible."""
        logger.info("👁️ Checking username blank error visibility")
        result = self.is_validation_error_visible(LOGIN_PAGE.ERROR_USERNAME_BLANK)
        logger.info(f"   Result: {result}")
        return result

    @log_method
    @log_page_state
    def click_default_company_link(self) -> SelfServicePage:
        """Click the default company link."""
        logger.info("🖱️ Clicking default company link")
        # Use link text to find and click DEFAULT
        self.click_element_by_text(LOGIN_PAGE.DEFAULT_LINK)
        logger.info("✅ Navigating to Self Service page")
        return SelfServicePage(self.driver)
