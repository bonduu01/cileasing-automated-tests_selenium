"""
Tests for User Login functionality.
"""

import pytest
import time
import logging
from config import settings
from pages import HomePage, LoginPage

logger = logging.getLogger(__name__)


class TestUserLogins:
    """Test suite for User Login functionalities."""

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.regression
    def test_go_to_home_page_with_pom(self, home_page: HomePage) -> None:
        """Verify home page loads correctly with Page Object Model."""
        logger.info("📋 Test: Go to home page")

        logger.info("📋 Step 1: Navigate to home page")
        home_page.go_to_home_page()

        logger.info("📋 Step 2: Verify home page loaded")
        home_page.verify_home_page_loads()

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_valid_credentials_with_pom(self, login_page: LoginPage) -> None:
        """Verify successful login with valid credentials using POM."""
        logger.info("📋 Test: Valid Credentials Login")

        logger.info("📋 Step 1: Navigate to login page")
        login_page.go_to_login_page()

        logger.info("📋 Step 2: Perform login")
        login_page.login_user(
            email=settings.test_username,
            password=settings.test_password
        )

        logger.info("📋 Step 3: Verify login successful")
        login_page.verify_login_successful_load_companies()

        logger.info("📋 Step 4: Click default company")
        self_service_page = login_page.click_default_company_link()

        logger.info("✅ Successfully navigated to Self Service page")

        logger.info("📋 Step 5: Verify self-service page loads")
        self_service_page.verify_self_service_page_loads()

        logger.info("📋 Step 6: Logout")
        self_service_page.click_to_logout()

        logger.info("✅ Test completed successfully")

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_wrong_username(self, login_page: LoginPage) -> None:
        """Verify login failure with incorrect username."""
        logger.info("📋 Test: Login with wrong username")

        logger.info("📋 Step 1: Navigate to login page")
        login_page.go_to_login_page()

        logger.info("📋 Step 2: Enter wrong username")
        login_page.enter_email(settings.test_wrong_username)

        logger.info("📋 Step 3: Enter correct password")
        login_page.enter_password(settings.test_password)

        logger.info("📋 Step 4: Click login button")
        login_page.click_login_button()

        logger.info("📋 Step 5: Verify error message")
        #login_page.verify_error_message()
        login_page.verify_error_toast_visible()

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_wrong_password(self, login_page: LoginPage) -> None:
        """Verify login failure with incorrect password."""
        logger.info("📋 Test: Login with wrong password")

        logger.info("📋 Step 1: Navigate to login page")
        login_page.go_to_login_page()

        logger.info("📋 Step 2: Enter correct username")
        login_page.enter_email(settings.test_username)

        logger.info("📋 Step 3: Enter wrong password")
        login_page.enter_password(settings.test_wrong_password)

        logger.info("📋 Step 4: Click login button")
        login_page.click_login_button()

        logger.info("📋 Step 5: Verify error message")
        #login_page.verify_error_message()
        login_page.verify_error_toast_visible()

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_no_password(self, login_page: LoginPage) -> None:
        """Verify validation error when password is not provided."""
        logger.info("📋 Test: Login with no password")

        logger.info("📋 Step 1: Navigate to login page")
        login_page.go_to_login_page()

        logger.info("📋 Step 2: Enter username only")
        login_page.enter_email(settings.test_wrong_username)

        logger.info("📋 Step 3: Click login button")
        login_page.click_login_button()

        logger.info("📋 Step 4: Verify password error")
        login_page.verify_password_blank_error()
        login_page.is_password_blank_error_visible()

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_no_username_or_password(self, login_page: LoginPage) -> None:
        """Verify validation errors when no credentials are provided."""
        logger.info("📋 Test: Login with no username")

        logger.info("📋 Step 1: Navigate to login page")
        login_page.go_to_login_page()

        logger.info("📋 Step 2: Click login button without entering credentials")
        login_page.click_login_button()

        logger.info("📋 Step 3: Verify username error")
        login_page.verify_username_blank_error()

        logger.info("📋 Step 4: Verify username error visible")
        login_page.is_username_blank_error_visible()

        logger.info("📋 Step 5: Verify password error visible")
        login_page.is_password_blank_error_visible()
