"""
Custom wait conditions for Selenium
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from typing import Callable
from utils.logger import logger


class CustomWaits:
    """Custom wait conditions"""

    @staticmethod
    def wait_for_url_contains(driver, url_fragment: str, timeout: int = 10) -> bool:
        """
        Wait for URL to contain specific fragment

        Args:
            driver: WebDriver instance
            url_fragment: URL fragment to check
            timeout: Maximum wait time

        Returns:
            bool: True if condition met
        """
        try:
            WebDriverWait(driver, timeout).until(
                EC.url_contains(url_fragment)
            )
            logger.info(f"URL contains: {url_fragment}")
            return True
        except TimeoutException:
            logger.error(f"URL does not contain: {url_fragment}")
            return False

    @staticmethod
    def wait_for_url_to_be(driver, url: str, timeout: int = 10) -> bool:
        """
        Wait for URL to be exact value

        Args:
            driver: WebDriver instance
            url: Expected URL
            timeout: Maximum wait time

        Returns:
            bool: True if condition met
        """
        try:
            WebDriverWait(driver, timeout).until(
                EC.url_to_be(url)
            )
            logger.info(f"URL is: {url}")
            return True
        except TimeoutException:
            logger.error(f"URL is not: {url}")
            return False

    @staticmethod
    def wait_for_element_text_to_be(driver, locator: tuple, text: str, timeout: int = 10) -> bool:
        """
        Wait for element text to be specific value

        Args:
            driver: WebDriver instance
            locator: Element locator
            text: Expected text
            timeout: Maximum wait time

        Returns:
            bool: True if condition met
        """
        try:
            WebDriverWait(driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            logger.info(f"Element contains text: {text}")
            return True
        except TimeoutException:
            logger.error(f"Element does not contain text: {text}")
            return False

    @staticmethod
    def wait_for_custom_condition(driver, condition: Callable, timeout: int = 10, poll_frequency: float = 0.5) -> bool:
        """
        Wait for custom condition

        Args:
            driver: WebDriver instance
            condition: Custom condition function
            timeout: Maximum wait time
            poll_frequency: How often to check condition

        Returns:
            bool: True if condition met
        """
        try:
            wait = WebDriverWait(driver, timeout, poll_frequency=poll_frequency)
            wait.until(condition)
            logger.info("Custom condition met")
            return True
        except TimeoutException:
            logger.error("Custom condition not met")
            return False