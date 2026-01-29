"""
Login page test cases
"""
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from config.settings import settings
from utils.logger import Logger

logger = Logger.get_logger(__name__)


@pytest.mark.login
class TestLogin:
    """Login test suite"""

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_successful_login(self, driver):
        """Test successful login with valid credentials"""
        logger.info("TEST: Successful login")

        login_page = LoginPage(driver)
        home_page = HomePage(driver)

        login_page.navigate_to_login_page()
        login_page.quick_login()

        assert home_page.is_user_logged_in(), "User should be logged in"
        assert home_page.is_logout_button_visible(), "Logout button should be visible"
        assert "logged-in-successfully" in driver.current_url, "URL should indicate success"

    @pytest.mark.regression
    @pytest.mark.parametrize("username,password,expected_error", [
        ("invalidUser", settings.valid_password, "invalid"),
        (settings.valid_username, "wrongPassword", "invalid"),
        ("", settings.valid_password, "invalid"),
        (settings.valid_username, "", "invalid"),
    ])
    def test_login_with_invalid_credentials(self, driver, username, password, expected_error):
        """Test login with invalid credentials"""
        logger.info(f"TEST: Invalid login - username: {username}")

        login_page = LoginPage(driver)

        login_page.navigate_to_login_page()
        login_page.login(username, password)

        assert login_page.is_error_message_displayed(), "Error message should be displayed"
        error_text = login_page.get_error_message().lower()
        assert expected_error in error_text, f"Error should contain '{expected_error}'"

    @pytest.mark.smoke
    def test_login_page_loads(self, driver):
        """Test login page loads correctly"""
        logger.info("TEST: Login page loads")

        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()

        assert "login" in driver.current_url.lower(), "URL should contain 'login'"
        assert login_page.is_login_button_enabled(), "Login button should be enabled"

        page_title = login_page.get_page_title()
        assert page_title, "Page should have a title"