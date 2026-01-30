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

# ------------------------------------------------------------------------------
# Directory setup
# ------------------------------------------------------------------------------
os.makedirs("screenshots", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("reports", exist_ok=True)


# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------
def setup_logging():
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info("🚀 TEST RUN STARTED")
    logger.info(f"   🌐 Browser: {settings.browser}")
    logger.info(f"   👁️ Headless: {settings.headless}")
    logger.info(f"   ⏱️  Explicit wait: {settings.explicit_wait}s")
    logger.info("=" * 80 + "\n")


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    setup_logging()
    yield
    logging.getLogger(__name__).info("\n" + "=" * 80 + "\n✅ TEST RUN COMPLETED\n" + "=" * 80)


# ------------------------------------------------------------------------------
# WebDriver Fixture
# ------------------------------------------------------------------------------
@pytest.fixture(scope="function")
def driver() -> Generator[webdriver.Remote, None, None]:
    logger = logging.getLogger(__name__)
    logger.info(f"🌐 Launching {settings.browser} (headless={settings.headless})")

    if settings.browser.lower() == "chrome":
        options = webdriver.ChromeOptions()

        if settings.headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        service = ChromeService(ChromeDriverManager().install())
        driver_instance = webdriver.Chrome(service=service, options=options)

    elif settings.browser.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        if settings.headless:
            options.add_argument("--headless")

        service = FirefoxService(GeckoDriverManager().install())
        driver_instance = webdriver.Firefox(service=service, options=options)

    elif settings.browser.lower() == "edge":
        options = webdriver.EdgeOptions()
        if settings.headless:
            options.add_argument("--headless")

        service = EdgeService(EdgeChromiumDriverManager().install())
        driver_instance = webdriver.Edge(service=service, options=options)

    else:
        raise ValueError(f"Unsupported browser: {settings.browser}")

    # Timeouts
    driver_instance.implicitly_wait(settings.implicit_wait)
    driver_instance.set_page_load_timeout(settings.page_load_timeout)

    # IMPORTANT: only resize/maximize when NOT headless
    if not settings.headless:
        if settings.maximize_window:
            driver_instance.maximize_window()
        else:
            driver_instance.set_window_size(
                settings.window_width, settings.window_height
            )

    logger.info("✅ Browser ready")
    yield driver_instance

    logger.info("🌐 Closing browser")
    driver_instance.quit()


# ------------------------------------------------------------------------------
# Page Fixtures
# ------------------------------------------------------------------------------
@pytest.fixture
def home_page(driver) -> HomePage:
    return HomePage(driver)


@pytest.fixture
def login_page(driver) -> LoginPage:
    return LoginPage(driver)


@pytest.fixture
def self_service_page(authenticated_driver) -> SelfServicePage:
    return SelfServicePage(authenticated_driver)


# ------------------------------------------------------------------------------
# Authenticated Driver Fixture
# ------------------------------------------------------------------------------
@pytest.fixture
def authenticated_driver(driver) -> Generator[webdriver.Remote, None, None]:
    logger = logging.getLogger(__name__)
    logger.info("\n" + "=" * 60)
    logger.info("🔐 AUTHENTICATION SETUP")
    logger.info("=" * 60)

    try:
        login_page = LoginPage(driver)

        login_page.go_to_login_page()
        login_page.login_user(
            email=settings.test_username,
            password=settings.test_password,
        )
        login_page.verify_login_successful_load_companies()

        self_service_page = login_page.click_default_company_link()
        self_service_page.verify_self_service_page_loads()

        logger.info("✅ Authentication successful")
        yield driver

    finally:
        logger.info("\n" + "=" * 60)
        logger.info("🔐 AUTHENTICATION TEARDOWN")
        logger.info("=" * 60)

        try:
            SelfServicePage(driver).click_to_logout()
            logger.info("✅ Logout successful")
        except Exception:
            logger.warning("⚠️ Logout skipped (page not available)")


# ------------------------------------------------------------------------------
# Pytest Hooks
# ------------------------------------------------------------------------------
def pytest_configure(config):
    config.addinivalue_line("markers", "smoke")
    config.addinivalue_line("markers", "regression")
    config.addinivalue_line("markers", "login")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    logger = logging.getLogger(__name__)

    if report.when == "call" and report.failed and settings.screenshot_on_failure:
        driver = item.funcargs.get("driver") or item.funcargs.get("authenticated_driver")
        if driver:
            ts = int(datetime.now().timestamp())
            name = item.name.replace(" ", "_")
            path = f"{settings.screenshot_dir}failure_{name}_{ts}.png"
            driver.save_screenshot(path)
            logger.error(f"📸 Screenshot saved: {path}")


@pytest.fixture(autouse=True)
def log_test_info(request):
    logger = logging.getLogger(__name__)
    logger.info("\n" + "#" * 80)
    logger.info(f"🧪 STARTING TEST: {request.node.name}")
    logger.info("#" * 80)
    yield
    logger.info("\n" + "#" * 80)
    logger.info(f"🏁 FINISHED TEST: {request.node.name}")
    logger.info("#" * 80)
