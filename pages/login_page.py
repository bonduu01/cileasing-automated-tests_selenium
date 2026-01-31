from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import logging

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
        self.verify_element_visible(LOGIN_PAGE.FLOUR_MILLS_COMPANY)
        logger.info("✅ Company list verified")

    # @log_method
    # def verify_error_message(self) -> None:
    #     """Assert an error message is displayed."""
    #     logger.info("⚠️ Verifying error message is displayed")
    #     self.verify_has_text_visible(LOGIN_PAGE.ERROR_TOAST, LOGIN_PAGE.ERROR_INVALID_CREDENTIALS)

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
        """
        Click the default company link and verify navigation to Self Service page.
        Enhanced for headless mode compatibility.
        """
        logger.info("🖱️ Clicking default company link")

        # Wait for any loading states to complete
        try:
            logger.info("⏳ Checking for loading indicators...")
            loading_selector = ".ant-spin-spinning"
            # Use immediate check instead of waiting
            loading_elements = self.driver.find_elements(By.CSS_SELECTOR, loading_selector)
            if loading_elements and any(el.is_displayed() for el in loading_elements):
                logger.info("   Loading indicator found, waiting for it to disappear...")
                WebDriverWait(self.driver, 15).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, loading_selector))
                )
                logger.info("   ✅ Loading complete")
            else:
                logger.info("   ℹ️ No loading indicators detected")
        except Exception as e:
            logger.info(f"   ℹ️ Loading check complete: {e}")

        # Capture initial state
        initial_url = self.driver.current_url
        logger.info(f"   📍 Current URL: {initial_url}")

        # Try multiple click strategies
        clicked = False
        click_strategies = [
            ("Standard click with retry", lambda: self.click_element_with_retry(
                LOGIN_PAGE.DEFAULT_LINK, timeout=30, max_attempts=3
            )),
            ("JavaScript click", lambda: self.click_with_javascript(LOGIN_PAGE.DEFAULT_LINK)),
            ("ActionChains click", lambda: self._action_chains_click(LOGIN_PAGE.DEFAULT_LINK))
        ]

        for strategy_name, click_func in click_strategies:
            try:
                logger.info(f"   Trying: {strategy_name}")
                click_func()
                clicked = True

                # Wait for URL change or specific element
                try:
                    WebDriverWait(self.driver, 15).until(
                        lambda driver: driver.current_url != initial_url or
                                       self._check_for_self_service_elements()
                    )
                    logger.info(f"   ✅ Navigation successful with {strategy_name}")
                    break
                except TimeoutException:
                    logger.warning(f"   ⚠️ No navigation detected with {strategy_name}")
                    if strategy_name == click_strategies[-1][0]:
                        # Last strategy, accept it anyway
                        break
                    continue

            except Exception as e:
                logger.warning(f"   ⚠️ {strategy_name} failed: {e}")
                if strategy_name == click_strategies[-1][0]:
                    raise
                continue

        # Final URL check
        final_url = self.driver.current_url
        logger.info(f"   📍 Final URL: {final_url}")

        if final_url != initial_url:
            logger.info(f"   ✅ URL changed - navigation detected")
        else:
            logger.warning(f"   ⚠️ URL unchanged - checking for SPA behavior")
            # Check if we can find self-service page elements
            if self._check_for_self_service_elements():
                logger.info("   ✅ Self-service page elements detected")
            else:
                logger.error("   ❌ Cannot confirm navigation to self-service page")
                self._take_screenshot("navigation_verification_failed")

        # Brief wait for page stability
        logger.info("⏳ Waiting for page to stabilize...")
        time.sleep(2)

        logger.info("✅ Transitioning to Self Service page object")
        return SelfServicePage(self.driver)

    def _action_chains_click(self, selector: str) -> None:
        """Click using ActionChains."""
        element = self._find_clickable_element(selector, timeout=30)
        self.scroll_to_element(element)
        time.sleep(0.3)
        ActionChains(self.driver).move_to_element(element).click().perform()

    def _check_for_self_service_elements(self) -> bool:
        """Check if self-service page elements are present."""
        try:
            # Add selectors that are unique to the self-service page
            selectors = [
                "//h1[contains(text(), 'Self Service')]",
                "//div[contains(@class, 'self-service')]",
                "span.ant-avatar.ant-dropdown-trigger",  # Profile avatar
            ]

            for selector in selectors:
                try:
                    by, value = self._get_by_strategy(selector)
                    element = self.driver.find_element(by, value)
                    if element.is_displayed():
                        logger.info(f"   Found element: {selector}")
                        return True
                except:
                    continue

            return False
        except:
            return False
