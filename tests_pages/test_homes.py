"""
Home page test cases
"""
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from config.settings import settings
from utils.logger import Logger

logger = Logger.get_logger(__name__)


@pytest.fixture(scope="function")
def logged_in_user(driver):
    """Fixture to log in user"""
    login_page = LoginPage(driver)
    home_page = HomePage(driver)

    login_page.navigate_to_login_page()
    login_page.quick_login()

    assert home_page.is_user_logged_in(), "User must be logged in"

    yield home_page


@pytest.mark.home
class TestHomePage:
    """Home page test suite"""

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_logout_button_visible(self, logged_in_user):
        """Test logout button is visible"""
        logger.info("TEST: Logout button visible")

        home_page = logged_in_user
        assert home_page.is_logout_button_visible(), "Logout button should be visible"

    @pytest.mark.regression
    def test_success_message_displayed(self, logged_in_user):
        """Test success message is displayed"""
        logger.info("TEST: Success message displayed")

        home_page = logged_in_user
        success_message = home_page.get_success_message()

        assert success_message, "Success message should exist"
        assert len(success_message) > 0, "Success message should not be empty"

    @pytest.mark.smoke
    def test_logout_functionality(self, logged_in_user, driver):
        """Test logout functionality"""
        logger.info("TEST: Logout functionality")

        home_page = logged_in_user
        login_page = LoginPage(driver)

        home_page.click_logout()

        assert "login" in driver.current_url.lower(), "Should redirect to login page"
        assert login_page.is_element_visible(login_page.LOGIN_BUTTON), "Login button should be visible"