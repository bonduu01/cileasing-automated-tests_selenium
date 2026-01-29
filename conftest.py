"""
Pytest configuration and fixtures for Selenium test framework.
"""

from typing import Generator
import logging
import sys
import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config import settings
from pages import HomePage, LoginPage, SelfServicePage

# Create necessary directories
os.makedirs("screenshots", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("reports", exist_ok=True)


def setup_logging():
    """Configure console logging for all tests."""
    # Configure root logger with console output
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Reduce noise from selenium and urllib3
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info(f"{'=' * 80}")
    logger.info(f"🚀 TEST RUN STARTED")
    logger.info(f"   📸 Screenshots: {settings.screenshot_dir}")
    logger.info(f"   🌐 Browser: {settings.browser}")
    logger.info(f"   👁️ Headless: {settings.headless}")
    logger.info(f"   ⏱️  Timeout: {settings.explicit_wait}s")
    logger.info(f"{'=' * 80}\n")


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """Auto-configure logging for all tests."""
    setup_logging()
    yield

    logger = logging.getLogger(__name__)
    logger.info(f"\n{'=' * 80}")
    logger.info(f"✅ TEST RUN COMPLETED")
    logger.info(f"{'=' * 80}")


# --- Core WebDriver Fixtures ---


@pytest.fixture(scope="function")
def driver() -> Generator[webdriver.Remote, None, None]:
    """
    Function-scoped WebDriver instance.
    Each test gets a fresh browser instance.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"🌐 Launching {settings.browser} browser (headless={settings.headless})")

    # Initialize driver based on browser setting
    driver_instance = None

    if settings.browser.lower() == "chrome":
        chrome_options = webdriver.ChromeOptions()

        if settings.headless:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        service = ChromeService(ChromeDriverManager().install())
        driver_instance = webdriver.Chrome(service=service, options=chrome_options)

    elif settings.browser.lower() == "firefox":
        firefox_options = webdriver.FirefoxOptions()

        if settings.headless:
            firefox_options.add_argument("--headless")

        service = FirefoxService(GeckoDriverManager().install())
        driver_instance = webdriver.Firefox(service=service, options=firefox_options)

    elif settings.browser.lower() == "edge":
        edge_options = webdriver.EdgeOptions()

        if settings.headless:
            edge_options.add_argument("--headless")

        edge_options.add_argument("--start-maximized")

        service = EdgeService(EdgeChromiumDriverManager().install())
        driver_instance = webdriver.Edge(service=service, options=edge_options)

    else:
        raise ValueError(f"Unsupported browser: {settings.browser}")

    # Configure driver timeouts
    driver_instance.implicitly_wait(settings.implicit_wait)
    driver_instance.set_page_load_timeout(settings.page_load_timeout)

    # Maximize window if configured
    if settings.maximize_window and not settings.headless:
        driver_instance.maximize_window()
    else:
        driver_instance.set_window_size(settings.window_width, settings.window_height)

    logger.info(f"   ✅ Browser launched: {settings.browser}")

    yield driver_instance

    logger.info(f"🌐 Closing {settings.browser} browser")
    driver_instance.quit()


# --- Page Object Fixtures ---


@pytest.fixture
def home_page(driver: webdriver.Remote) -> HomePage:
    """HomePage fixture."""
    logger = logging.getLogger(__name__)
    logger.info("🏗️ Creating HomePage fixture")
    return HomePage(driver)


@pytest.fixture
def login_page(driver: webdriver.Remote) -> LoginPage:
    """LoginPage fixture."""
    logger = logging.getLogger(__name__)
    logger.info("🏗️ Creating LoginPage fixture")
    return LoginPage(driver)


@pytest.fixture
def self_service_page(authenticated_driver: webdriver.Remote) -> SelfServicePage:
    """Self Service Page fixture."""
    logger = logging.getLogger(__name__)
    logger.info("🏗️ Creating SelfServicePage fixture")
    return SelfServicePage(authenticated_driver)


# --- Utility Fixtures ---


@pytest.fixture
def authenticated_driver(driver: webdriver.Remote) -> Generator[webdriver.Remote, None, None]:
    """
    Driver fixture that is already authenticated.
    Useful for tests that require a logged-in state.
    """
    logger = logging.getLogger(__name__)
    logger.info("\n" + "=" * 60)
    logger.info("🔐 AUTHENTICATION SETUP")
    logger.info("=" * 60)

    try:
        login_page = LoginPage(driver)

        logger.info("📋 Step 1: Navigate to login page")
        login_page.go_to_login_page()

        logger.info("📋 Step 2: Perform login")
        login_page.login_user(
            email=settings.test_username,
            password=settings.test_password
        )

        logger.info("📋 Step 3: Verify login successful")
        login_page.verify_login_successful_load_companies()

        logger.info("📋 Step 4: Click default company link")
        self_service_page = login_page.click_default_company_link()

        logger.info("📋 Step 5: Verify self-service page loads")
        self_service_page.verify_self_service_page_loads()

        logger.info("✅ Authentication successful")
        logger.info("=" * 60 + "\n")

        yield driver

        # Teardown (logout)
        logger.info("\n" + "=" * 60)
        logger.info("🔐 AUTHENTICATION TEARDOWN")
        logger.info("=" * 60)
        logger.info("📋 Logging out...")

        self_service_page.click_to_logout()

        logger.info("✅ Logout successful")
        logger.info("=" * 60 + "\n")

    except Exception as e:
        logger.error(f"❌ Authentication setup failed: {e}")

        # Take screenshot on failure
        try:
            timestamp = int(datetime.now().timestamp())
            screenshot_path = f"{settings.screenshot_dir}auth_error_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
            logger.error(f"   📸 Error screenshot: {screenshot_path}")
        except:
            pass

        raise


# --- Pytest Hooks ---


def pytest_configure(config):
    """Configure custom pytest markers."""
    logger = logging.getLogger(__name__)
    logger.info("⚙️ Configuring pytest markers")

    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "login: mark test as login-related")


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on markers or config."""
    logger = logging.getLogger(__name__)
    logger.info(f"📊 Collected {len(items)} test(s)")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to log test results and take screenshots on failure."""
    outcome = yield
    report = outcome.get_result()

    logger = logging.getLogger(__name__)

    if report.when == "call":
        if report.passed:
            logger.info(f"✅ TEST PASSED: {item.nodeid}")
        elif report.failed:
            logger.error(f"❌ TEST FAILED: {item.nodeid}")
            logger.error(f"   Failure reason: {str(report.longrepr)[:200]}...")

            # Take screenshot on failure if enabled
            if settings.screenshot_on_failure:
                try:
                    driver = item.funcargs.get('driver') or item.funcargs.get('authenticated_driver')
                    if driver:
                        timestamp = int(datetime.now().timestamp())
                        test_name = item.name.replace(" ", "_").replace("/", "_")
                        screenshot_path = f"{settings.screenshot_dir}failure_{test_name}_{timestamp}.png"
                        driver.save_screenshot(screenshot_path)
                        logger.error(f"   📸 Failure screenshot: {screenshot_path}")
                except Exception as e:
                    logger.warning(f"   ⚠️ Could not take failure screenshot: {e}")

        elif report.skipped:
            logger.warning(f"⏭️ TEST SKIPPED: {item.nodeid}")


@pytest.fixture(autouse=True)
def log_test_info(request):
    """Automatically log test start and end for each test."""
    logger = logging.getLogger(__name__)
    test_name = request.node.name

    logger.info(f"\n{'#' * 80}")
    logger.info(f"🧪 STARTING TEST: {test_name}")
    logger.info(f"{'#' * 80}\n")

    yield

    logger.info(f"\n{'#' * 80}")
    logger.info(f"🏁 FINISHED TEST: {test_name}")
    logger.info(f"{'#' * 80}\n")
