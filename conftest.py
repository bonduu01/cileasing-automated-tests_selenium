"""
Enhanced Pytest Configuration with Advanced Features
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.settings import settings
from utils.logger import Logger
from datetime import datetime
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

logger = Logger.get_logger(__name__)


def pytest_addoption(parser):
    """Add custom command-line options"""
    parser.addoption(
        "--browser",
        action="store",
        default=settings.browser,
        help="Browser: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=settings.headless,
        help="Run in headless mode"
    )
    parser.addoption(
        "--env",
        action="store",
        default=settings.environment,
        help="Environment: dev, qa, staging, prod"
    )


def pytest_configure(config):
    """Configure pytest"""
    # Print configuration
    logger.info("=" * 70)
    logger.info("TEST EXECUTION STARTED")
    logger.info("=" * 70)
    settings.print_settings()

    # Register custom markers
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression tests")
    config.addinivalue_line("markers", "login: Login tests")
    config.addinivalue_line("markers", "home: Home page tests")
    config.addinivalue_line("markers", "critical: Critical path tests")
    config.addinivalue_line("markers", "slow: Slow running tests")


@pytest.fixture(scope="function")
def driver(request):
    """
    WebDriver fixture with setup and teardown

    Yields:
        WebDriver: Configured WebDriver instance
    """
    browser_name = request.config.getoption("--browser")
    headless_mode = request.config.getoption("--headless")

    logger.info(f"Setting up {browser_name} browser (headless: {headless_mode})")

    # Initialize driver
    if browser_name.lower() == "chrome":
        driver = _setup_chrome_driver(headless_mode)
    elif browser_name.lower() == "firefox":
        driver = _setup_firefox_driver(headless_mode)
    elif browser_name.lower() == "edge":
        driver = _setup_edge_driver(headless_mode)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    # Configure driver
    driver.maximize_window()
    driver.implicitly_wait(settings.implicit_wait)
    driver.set_page_load_timeout(settings.page_load_timeout)

    # Log test info
    logger.info(f"Starting test: {request.node.name}")

    yield driver

    # Teardown
    if request.node.rep_call.failed and settings.screenshot_on_failure:
        _take_failure_screenshot(driver, request.node.nodeid)

    logger.info(f"Closing browser for test: {request.node.name}")
    driver.quit()


def _setup_chrome_driver(headless: bool):
    """Setup Chrome driver"""
    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument(f"--window-size={settings.window_size}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    logger.info("Chrome driver initialized")
    return driver


def _setup_firefox_driver(headless: bool):
    """Setup Firefox driver"""
    options = webdriver.FirefoxOptions()

    if headless:
        options.add_argument("--headless")

    width, height = settings.get_window_size_tuple()
    options.add_argument(f"--width={width}")
    options.add_argument(f"--height={height}")

    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    logger.info("Firefox driver initialized")
    return driver


def _setup_edge_driver(headless: bool):
    """Setup Edge driver"""
    options = webdriver.EdgeOptions()

    if headless:
        options.add_argument("--headless")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--window-size={settings.window_size}")

    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)

    logger.info("Edge driver initialized")
    return driver


def _take_failure_screenshot(driver, nodeid: str):
    """Take screenshot on test failure"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = nodeid.replace("/", "_").replace("::", "_").replace(" ", "_")
        screenshot_name = f"FAILED_{test_name}_{timestamp}.png"
        screenshot_path = settings.screenshots_dir / screenshot_name

        driver.save_screenshot(str(screenshot_path))
        logger.info(f"Failure screenshot: {screenshot_path}")
    except Exception as e:
        logger.error(f"Failed to take screenshot: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test result for screenshot"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_sessionfinish(session, exitstatus):
    """Hook called after test session"""
    logger.info("=" * 70)
    logger.info("TEST EXECUTION COMPLETED")
    logger.info(f"Exit Status: {exitstatus}")
    logger.info("=" * 70)