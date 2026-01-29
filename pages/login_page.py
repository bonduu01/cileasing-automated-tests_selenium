"""
Login Page Object Model
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import settings
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class LoginPage(BasePage):
    """Login Page class"""

    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "submit")
    ERROR_MESSAGE = (By.ID, "error")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")

    def __init__(self, driver):
        """Initialize Login Page"""
        super().__init__(driver)
        logger.info("Login Page initialized")

    def navigate_to_login_page(self):
        """Navigate to login page"""
        self.open_url(settings.login_url)
        logger.info(f"Navigated to login page: {settings.login_url}")

    def enter_username(self, username: str):
        """Enter username"""
        self.type_text(self.USERNAME_INPUT, username)
        logger.info(f"Entered username: {username}")

    def enter_password(self, password: str):
        """Enter password"""
        self.type_text(self.PASSWORD_INPUT, password)
        logger.info("Entered password: ****")

    def click_login_button(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
        logger.info("Clicked login button")

    def login(self, username: str, password: str):
        """Perform complete login"""
        logger.info(f"Attempting login with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def quick_login(self):
        """Quick login with default credentials"""
        self.login(settings.valid_username, settings.valid_password)

    def get_error_message(self) -> str:
        """Get error message text"""
        error_text = self.get_text(self.ERROR_MESSAGE)
        logger.info(f"Error message: {error_text}")
        return error_text

    def is_error_message_displayed(self) -> bool:
        """Check if error message is displayed"""
        is_displayed = self.is_element_visible(self.ERROR_MESSAGE, timeout=5)
        logger.info(f"Error message displayed: {is_displayed}")
        return is_displayed

    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled"""
        element = self.find_element(self.LOGIN_BUTTON)
        is_enabled = element.is_enabled()
        logger.info(f"Login button enabled: {is_enabled}")
        return is_enabled