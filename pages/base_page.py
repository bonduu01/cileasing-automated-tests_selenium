"""
Enhanced Base Page with advanced features
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from config.settings import settings
from utils.logger import Logger
from typing import List, Optional
from datetime import datetime

logger = Logger.get_logger(__name__)


class BasePage:
    """Enhanced Base Page with advanced features"""

    def __init__(self, driver):
        """Initialize BasePage with driver"""
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.explicit_wait)
        self.short_wait = WebDriverWait(driver, 5)
        self.actions = ActionChains(driver)

    # ==================== Navigation ====================
    def open_url(self, url: str):
        """Open URL"""
        logger.info(f"Opening URL: {url}")
        self.driver.get(url)
        self.wait_for_page_load()

    def refresh_page(self):
        """Refresh current page"""
        logger.info("Refreshing page")
        self.driver.refresh()
        self.wait_for_page_load()

    def go_back(self):
        """Navigate back"""
        logger.info("Navigating back")
        self.driver.back()

    def go_forward(self):
        """Navigate forward"""
        logger.info("Navigating forward")
        self.driver.forward()

    # ==================== Element Interaction ====================
    def find_element(self, locator: tuple, timeout: Optional[int] = None):
        """Find element with retry logic"""
        timeout = timeout or settings.explicit_wait
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                wait = WebDriverWait(self.driver, timeout)
                element = wait.until(EC.presence_of_element_located(locator))
                logger.info(f"Element found: {locator}")
                return element
            except StaleElementReferenceException:
                if attempt == max_attempts - 1:
                    logger.error(f"Element stale after {max_attempts} attempts: {locator}")
                    raise
                logger.warning(f"Stale element, retrying... (attempt {attempt + 1})")
            except TimeoutException:
                logger.error(f"Element not found: {locator}")
                self.take_screenshot(f"element_not_found_{locator[1]}")
                raise

    def find_elements(self, locator: tuple) -> List:
        """Find multiple elements"""
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            logger.info(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            logger.warning(f"No elements found: {locator}")
            return []

    def click(self, locator: tuple):
        """Click element with wait"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        logger.info(f"Clicked: {locator}")

    def click_with_js(self, locator: tuple):
        """Click using JavaScript"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)
        logger.info(f"Clicked with JS: {locator}")

    def type_text(self, locator: tuple, text: str, clear_first: bool = True):
        """Type text into element"""
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.info(f"Typed text into {locator}: {text}")

    def type_text_slowly(self, locator: tuple, text: str, delay: float = 0.1):
        """Type text character by character"""
        element = self.find_element(locator)
        element.clear()
        for char in text:
            element.send_keys(char)
            import time
            time.sleep(delay)
        logger.info(f"Typed text slowly: {locator}")

    def get_text(self, locator: tuple) -> str:
        """Get element text"""
        element = self.find_element(locator)
        text = element.text
        logger.info(f"Got text from {locator}: {text}")
        return text

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """Get attribute value"""
        element = self.find_element(locator)
        value = element.get_attribute(attribute)
        logger.info(f"Got attribute '{attribute}' from {locator}: {value}")
        return value

    # ==================== Visibility Checks ====================
    def is_element_visible(self, locator: tuple, timeout: Optional[int] = None) -> bool:
        """Check if element is visible"""
        timeout = timeout or settings.explicit_wait
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            logger.info(f"Element visible: {locator}")
            return True
        except TimeoutException:
            logger.info(f"Element not visible: {locator}")
            return False

    def is_element_present(self, locator: tuple) -> bool:
        """Check if element is present in DOM"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def is_element_clickable(self, locator: tuple, timeout: int = 5) -> bool:
        """Check if element is clickable"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_element_to_disappear(self, locator: tuple, timeout: Optional[int] = None) -> bool:
        """Wait for element to disappear"""
        timeout = timeout or settings.explicit_wait
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.invisibility_of_element_located(locator))
            logger.info(f"Element disappeared: {locator}")
            return True
        except TimeoutException:
            logger.error(f"Element did not disappear: {locator}")
            return False

    # ==================== Advanced Actions ====================
    def scroll_to_element(self, locator: tuple):
        """Scroll to element"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        logger.info(f"Scrolled to: {locator}")

    def hover_over_element(self, locator: tuple):
        """Hover over element"""
        element = self.find_element(locator)
        self.actions.move_to_element(element).perform()
        logger.info(f"Hovered over: {locator}")

    def double_click(self, locator: tuple):
        """Double click element"""
        element = self.find_element(locator)
        self.actions.double_click(element).perform()
        logger.info(f"Double clicked: {locator}")

    def right_click(self, locator: tuple):
        """Right click element"""
        element = self.find_element(locator)
        self.actions.context_click(element).perform()
        logger.info(f"Right clicked: {locator}")

    def drag_and_drop(self, source_locator: tuple, target_locator: tuple):
        """Drag and drop"""
        source = self.find_element(source_locator)
        target = self.find_element(target_locator)
        self.actions.drag_and_drop(source, target).perform()
        logger.info(f"Dragged {source_locator} to {target_locator}")

    # ==================== Page Information ====================
    def get_current_url(self) -> str:
        """Get current URL"""
        url = self.driver.current_url
        logger.info(f"Current URL: {url}")
        return url

    def get_page_title(self) -> str:
        """Get page title"""
        title = self.driver.title
        logger.info(f"Page title: {title}")
        return title

    def wait_for_page_load(self):
        """Wait for page to load completely"""
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        logger.info("Page loaded completely")

    # ==================== Screenshots ====================
    def take_screenshot(self, name: str) -> str:
        """Take screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{name}_{timestamp}.png"
        screenshot_path = settings.screenshots_dir / screenshot_name

        self.driver.save_screenshot(str(screenshot_path))
        logger.info(f"Screenshot saved: {screenshot_path}")
        return str(screenshot_path)

    # ==================== JavaScript Execution ====================
    def execute_script(self, script: str, *args):
        """Execute JavaScript"""
        return self.driver.execute_script(script, *args)

    def scroll_to_top(self):
        """Scroll to top of page"""
        self.execute_script("window.scrollTo(0, 0);")
        logger.info("Scrolled to top")

    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logger.info("Scrolled to bottom")

    # ==================== Frames & Windows ====================
    def switch_to_frame(self, locator: tuple):
        """Switch to iframe"""
        frame = self.find_element(locator)
        self.driver.switch_to.frame(frame)
        logger.info(f"Switched to frame: {locator}")

    def switch_to_default_content(self):
        """Switch to default content"""
        self.driver.switch_to.default_content()
        logger.info("Switched to default content")

    def switch_to_window(self, window_handle: str):
        """Switch to window"""
        self.driver.switch_to.window(window_handle)
        logger.info(f"Switched to window: {window_handle}")

    def get_window_handles(self) -> List[str]:
        """Get all window handles"""
        return self.driver.window_handles

    # ==================== Alerts ====================
    def accept_alert(self):
        """Accept alert"""
        alert = self.wait.until(EC.alert_is_present())
        alert.accept()
        logger.info("Alert accepted")

    def dismiss_alert(self):
        """Dismiss alert"""
        alert = self.wait.until(EC.alert_is_present())
        alert.dismiss()
        logger.info("Alert dismissed")

    def get_alert_text(self) -> str:
        """Get alert text"""
        alert = self.wait.until(EC.alert_is_present())
        text = alert.text
        logger.info(f"Alert text: {text}")
        return text