# pages/base_page.py

"""
Base Page Object providing common interactions for all page objects.
Selenium implementation with modern best practices.
"""

from __future__ import annotations

import os
import re
import logging
import time
from typing import TYPE_CHECKING, List, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementNotInteractableException,
)

from utils.decorators import log_method

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all Page Objects with common functionality."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.short_wait = WebDriverWait(driver, 5)
        self.actions = ActionChains(driver)
        logger.info(f"🏗️ Initialized {self.__class__.__name__}")

    # --- Helper Methods for Locator Strategy ---

    def _get_by_strategy(self, selector: str) -> Tuple[str, str]:
        """
        Determine the locator strategy based on selector format.

        Supported formats:
        - CSS Selector (default): 'div.class', '#id', '[name="value"]'
        - XPath: '//div[@class="value"]' or 'xpath://div'
        - ID: 'id=element_id'
        - Name: 'name=element_name'
        - Link Text: 'link=Link Text'
        - Partial Link Text: 'partial_link=Partial Text'
        - Tag Name: 'tag=div'
        - Class Name: 'class=classname'

        Returns:
            Tuple of (By strategy, selector value)
        """
        if selector.startswith('xpath=') or selector.startswith('//') or selector.startswith('(//'):
            return By.XPATH, selector.replace('xpath=', '')
        elif selector.startswith('id='):
            return By.ID, selector.replace('id=', '')
        elif selector.startswith('name='):
            return By.NAME, selector.replace('name=', '')
        elif selector.startswith('link='):
            return By.LINK_TEXT, selector.replace('link=', '')
        elif selector.startswith('partial_link='):
            return By.PARTIAL_LINK_TEXT, selector.replace('partial_link=', '')
        elif selector.startswith('tag='):
            return By.TAG_NAME, selector.replace('tag=', '')
        elif selector.startswith('class='):
            return By.CLASS_NAME, selector.replace('class=', '')
        else:
            # Default to CSS Selector
            return By.CSS_SELECTOR, selector

    def _find_element(self, selector: str, timeout: int = 30) -> WebElement:
        """Find a single element with wait."""
        by, value = self._get_by_strategy(selector)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def _find_elements(self, selector: str, timeout: int = 30) -> List[WebElement]:
        """Find multiple elements with wait."""
        by, value = self._get_by_strategy(selector)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located((by, value)))

    def _find_clickable_element(self, selector: str, timeout: int = 30) -> WebElement:
        """Find an element and ensure it's clickable."""
        by, value = self._get_by_strategy(selector)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))

    # --- Navigation ---

    @log_method
    def navigate_to(self, url: str) -> None:
        """Navigate to a URL."""
        logger.info(f"🌐 URL: {url}")
        try:
            self.driver.get(url)
            logger.info(f"   ✅ Navigation successful")
        except Exception as e:
            logger.error(f"   ❌ Navigation failed: {e}")
            self._take_screenshot("navigation_error")
            raise

    @log_method
    def reload(self) -> None:
        """Reload the current page."""
        logger.info("🔄 Reloading page")
        self.driver.refresh()

    @log_method
    def go_back(self) -> None:
        """Navigate back in browser history."""
        logger.info("⬅️ Going back")
        self.driver.back()

    @log_method
    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        logger.info("➡️ Going forward")
        self.driver.forward()

    # --- Element Interaction ---

    @log_method
    def click_element_with_retry(self, selector: str, timeout: int = 30, max_attempts: int = 3) -> None:
        """
        Click an element with retry logic and multiple strategies.
        Useful for stubborn elements or those that may have overlays.

        Args:
            selector: Selector string (supports multiple strategies)
            timeout: Timeout in seconds (default: 30)
            max_attempts: Number of retry attempts (default: 3)
        """
        logger.info(f"🖱️ Click with retry - Selector: {selector}, Max attempts: {max_attempts}")

        last_exception = None

        for attempt in range(1, max_attempts + 1):
            try:
                logger.info(f"   Attempt {attempt}/{max_attempts}")

                # Wait for element to be clickable
                element = self._find_clickable_element(selector, timeout)

                # Log element state
                self._log_element_state(element, selector)

                # Scroll into view
                self.scroll_to_element(element)

                # Wait a moment for any animations to complete
                time.sleep(0.3)

                # Try different click strategies
                if attempt == 1:
                    # Strategy 1: Standard click
                    logger.info("   📌 Strategy: Standard click")
                    element.click()
                elif attempt == 2:
                    # Strategy 2: JavaScript click
                    logger.info("   📌 Strategy: JavaScript click")
                    self.driver.execute_script("arguments[0].click();", element)
                else:
                    # Strategy 3: ActionChains click
                    logger.info("   📌 Strategy: ActionChains click")
                    ActionChains(self.driver).move_to_element(element).click().perform()

                # Verify click success by checking for URL change or element state
                time.sleep(0.5)
                logger.info(f"   ✅ Click successful on attempt {attempt}")
                return

            except (ElementNotInteractableException, StaleElementReferenceException) as e:
                last_exception = e
                logger.warning(f"   ⚠️ Attempt {attempt} failed: {e.__class__.__name__}")

                if attempt < max_attempts:
                    logger.info(f"   🔄 Retrying...")
                    time.sleep(1)
                else:
                    logger.error(f"   ❌ All {max_attempts} attempts failed")
                    self._take_screenshot("click_retry_failed")
                    raise

            except Exception as e:
                logger.error(f"   ❌ Unexpected error on attempt {attempt}: {e}")
                self._take_screenshot(f"click_error_attempt_{attempt}")
                raise

        # If we get here, all attempts failed
        if last_exception:
            raise last_exception

    @log_method
    def wait_for_no_overlays(self, timeout: int = 10) -> None:
        """
        Wait for common overlay/modal elements to disappear.
        Useful before interacting with elements that might be obscured.
        """
        logger.info("🔍 Checking for overlays/modals...")

        overlay_selectors = [
            ".ant-modal-mask",
            ".ant-drawer-mask",
            ".ant-spin-blur",
            ".ant-spin-spinning",
            "[class*='loading']",
            "[class*='overlay']"
        ]

        for selector in overlay_selectors:
            try:
                # Use short timeout to quickly check if overlay exists
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and any(el.is_displayed() for el in elements):
                    logger.info(f"   Found overlay: {selector}, waiting for it to disappear...")
                    WebDriverWait(self.driver, timeout).until(
                        EC.invisibility_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    logger.info(f"   ✅ Overlay {selector} disappeared")
            except (TimeoutException, StaleElementReferenceException):
                # Overlay didn't disappear in time or became stale (which is fine)
                logger.debug(f"   Overlay {selector} handling complete")
                pass
            except Exception as e:
                logger.debug(f"   Skipping overlay check for {selector}: {e}")
                pass

        logger.info("   ✅ No overlays detected")

    @log_method
    def click_element(self, selector: str, timeout: int = 30, verify_click: bool = True) -> None:
        """
        Click an element identified by selector with proper waits and optional verification.

        Args:
            selector: Selector string (supports multiple strategies)
            timeout: Timeout in seconds (default: 30)
            verify_click: Whether to verify click was registered (default: True)
        """
        logger.info(f"🖱️ Selector: {selector}")
        try:
            element = self._find_clickable_element(selector, timeout)

            # Log element state before interaction
            self._log_element_state(element, selector)

            # Store element state before click (for verification)
            initial_state = None
            if verify_click:
                initial_state = {
                    'is_displayed': element.is_displayed(),
                    'is_enabled': element.is_enabled(),
                    'location': element.location
                }

            # Scroll into view if needed
            self.scroll_to_element_by_selector(selector)

            # Click the element
            element.click()

            # Verify click was registered
            if verify_click:
                self._verify_click_registered(selector, initial_state)

            logger.info(f"   ✅ Click successful")
        except Exception as e:
            logger.error(f"   ❌ Click failed: {e}")
            self._take_screenshot("click_error")
            raise

    def _verify_click_registered(self, selector: str, initial_state: dict, timeout: int = 5) -> None:
        """
        Verify that a click was registered by checking for state changes.

        Args:
            selector: The element selector
            initial_state: Dictionary containing element's initial state
            timeout: Timeout for verification
        """
        try:
            # Wait for a brief moment to allow UI updates
            time.sleep(0.5)

            # Try to find the element again to check state changes
            try:
                element = self._find_element(selector, timeout=2)
                current_state = {
                    'is_displayed': element.is_displayed(),
                    'is_enabled': element.is_enabled(),
                    'location': element.location
                }

                # Check if element state changed (might indicate interaction)
                if current_state != initial_state:
                    logger.info("   🔍 Element state changed - click likely registered")
            except:
                # Element not found - might have been removed/hidden after click (expected behavior)
                logger.info("   🔍 Element no longer visible - click likely registered")

        except Exception as e:
            logger.warning(f"   ⚠️ Could not verify click: {e}")

    @log_method
    def click_element_by_text(self, text: str, timeout: int = 30) -> None:
        """Click an element containing specific text."""
        logger.info(f"🖱️ Clicking element with text: {text}")
        try:
            selector = f"//*[contains(text(), '{text}')]"
            self.click_element(selector, timeout)
        except Exception as e:
            logger.error(f"   ❌ Click by text failed: {e}")
            raise

    @log_method
    def click_with_javascript(self, selector: str) -> None:
        """Click an element using JavaScript (useful for hidden or problematic elements)."""
        logger.info(f"🖱️ JS Click - Selector: {selector}")
        element = self._find_element(selector)
        self.driver.execute_script("arguments[0].click();", element)
        logger.info(f"   ✅ JS Click successful")

    @log_method
    def fill_input(self, selector: str, value: str, timeout: int = 30, clear_first: bool = True) -> None:
        """Fill an input field with the specified value."""
        logger.info(f"✍️ Selector: {selector}, Value: {value}")
        try:
            element = self._find_element(selector, timeout)

            # Log element state
            self._log_element_state(element, selector)

            # Scroll into view
            self.scroll_to_element_by_selector(selector)

            # Clear if requested
            if clear_first:
                element.clear()

            # Fill the input
            element.send_keys(value)

            # Verify value was set
            actual_value = element.get_attribute('value')
            if actual_value != value:
                logger.warning(f"   ⚠️ Value mismatch: expected '{value}', got '{actual_value}'")

            logger.info(f"   ✅ Fill successful")
        except Exception as e:
            logger.error(f"   ❌ Fill failed: {e}")
            self._take_screenshot("fill_error")
            raise

    @log_method
    def type_text(self, selector: str, text: str, delay: float = 0.1) -> None:
        """Type text into an element character by character with delay."""
        logger.info(f"⌨️ Selector: {selector}, Text length: {len(text)}, Delay: {delay}s")
        element = self._find_element(selector)
        for char in text:
            element.send_keys(char)
            time.sleep(delay)

    @log_method
    def clear_input(self, selector: str) -> None:
        """Clear the content of an input field."""
        logger.info(f"🧹 Clearing: {selector}")
        element = self._find_element(selector)
        element.clear()

    @log_method
    def press_key(self, selector: str, key: str) -> None:
        """Press a specific key in an element."""
        logger.info(f"⌨️ Pressing key: {key} in {selector}")
        element = self._find_element(selector)

        # Map common key names to Keys constants
        key_mapping = {
            'ENTER': Keys.ENTER,
            'RETURN': Keys.RETURN,
            'TAB': Keys.TAB,
            'ESCAPE': Keys.ESCAPE,
            'ESC': Keys.ESCAPE,
            'BACKSPACE': Keys.BACKSPACE,
            'DELETE': Keys.DELETE,
            'SPACE': Keys.SPACE,
            'UP': Keys.ARROW_UP,
            'DOWN': Keys.ARROW_DOWN,
            'LEFT': Keys.ARROW_LEFT,
            'RIGHT': Keys.ARROW_RIGHT,
        }

        key_to_press = key_mapping.get(key.upper(), key)
        element.send_keys(key_to_press)

    def check_checkbox(self, selector: str) -> None:
        """Check a checkbox or radio button."""
        logger.info(f"☑️ Checking: {selector}")
        element = self._find_element(selector)
        if not element.is_selected():
            element.click()

    def uncheck_checkbox(self, selector: str) -> None:
        """Uncheck a checkbox."""
        logger.info(f"☐ Unchecking: {selector}")
        element = self._find_element(selector)
        if element.is_selected():
            element.click()

    def select_dropdown_option(self, selector: str, value: str = None, text: str = None, index: int = None) -> None:
        """
        Select an option from a dropdown (works with native <select> elements).

        Args:
            selector: Selector for the <select> element
            value: Select by value attribute
            text: Select by visible text
            index: Select by index (0-based)
        """
        logger.info(f"📋 Selecting dropdown: {selector}, Value: {value}, Text: {text}, Index: {index}")
        element = self._find_element(selector)
        select = Select(element)

        if value is not None:
            select.select_by_value(value)
        elif text is not None:
            select.select_by_visible_text(text)
        elif index is not None:
            select.select_by_index(index)
        else:
            raise ValueError("Must provide either value, text, or index")

    @log_method
    def click_ant_dropdown_item(self, dropdown_trigger_selector: str, menu_item_text: str, timeout: int = 30) -> None:
        """
        Click an item in an Ant Design dropdown menu.
        Handles opening the dropdown and selecting the menu item.

        Args:
            dropdown_trigger_selector: Selector for the dropdown trigger element
            menu_item_text: Text of the menu item to click
            timeout: Timeout in seconds
        """
        logger.info(f"📋 Ant Dropdown - Trigger: {dropdown_trigger_selector}, Item: {menu_item_text}")

        try:
            # Step 1: Wait for any loading/overlays to clear
            self.wait_for_no_overlays(timeout=5)

            # Step 2: Find and click the dropdown trigger
            logger.info("   🖱️ Step 1: Opening dropdown...")
            trigger_element = self._find_clickable_element(dropdown_trigger_selector, timeout)

            # Log trigger state
            self._log_element_state(trigger_element, dropdown_trigger_selector)

            # Scroll into view
            self.scroll_to_element(trigger_element)
            time.sleep(0.3)

            # Click to open dropdown
            trigger_element.click()
            logger.info("   ✅ Dropdown trigger clicked")

            # Step 3: Wait for dropdown menu to appear
            logger.info("   ⏳ Step 2: Waiting for dropdown menu...")
            dropdown_menu_selector = ".ant-dropdown:not(.ant-dropdown-hidden)"

            try:
                dropdown_menu = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, dropdown_menu_selector))
                )
                logger.info("   ✅ Dropdown menu visible")
            except TimeoutException:
                logger.error("   ❌ Dropdown menu did not appear")
                self._take_screenshot("dropdown_not_visible")
                raise

            # Step 4: Wait for menu item and click it
            logger.info(f"   🖱️ Step 3: Clicking menu item '{menu_item_text}'...")

            # Try multiple selector strategies for the menu item
            menu_item_selectors = [
                f"//li[contains(@class, 'ant-dropdown-menu-item')]//span[contains(text(), '{menu_item_text}')]",
                f"//li[contains(@class, 'ant-dropdown-menu-item')]//*[contains(text(), '{menu_item_text}')]",
                f".ant-dropdown-menu-item:has(*:contains('{menu_item_text}'))",
            ]

            menu_item_clicked = False
            last_exception = None

            for selector in menu_item_selectors:
                try:
                    by, value = self._get_by_strategy(selector)
                    menu_item = WebDriverWait(dropdown_menu, 5).until(
                        EC.element_to_be_clickable((by, value))
                    )

                    # Log menu item state
                    self._log_element_state(menu_item, selector)

                    # Click the menu item
                    menu_item.click()
                    logger.info(f"   ✅ Menu item '{menu_item_text}' clicked")
                    menu_item_clicked = True
                    break

                except Exception as e:
                    last_exception = e
                    logger.debug(f"   Selector '{selector}' failed: {e}")
                    continue

            if not menu_item_clicked:
                logger.error(f"   ❌ Could not find or click menu item '{menu_item_text}'")
                self._take_screenshot("menu_item_not_found")
                raise last_exception if last_exception else Exception(f"Menu item '{menu_item_text}' not found")

            # Step 5: Wait for dropdown to close (indicates action completed)
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, dropdown_menu_selector))
                )
                logger.info("   ✅ Dropdown closed - action completed")
            except TimeoutException:
                logger.warning("   ⚠️ Dropdown did not close, but continuing...")

        except Exception as e:
            logger.error(f"   ❌ Ant Dropdown interaction failed: {e}")
            self._take_screenshot("ant_dropdown_error")
            raise

    @log_method
    def click_ant_dropdown_trigger(self, selector: str, timeout: int = 30) -> None:
        """
        Click an Ant Design dropdown trigger and wait for menu to appear.

        Args:
            selector: Selector for the dropdown trigger
            timeout: Timeout in seconds
        """
        logger.info(f"📋 Opening Ant Dropdown: {selector}")

        try:
            # Wait for overlays to clear
            self.wait_for_no_overlays(timeout=5)

            # Find and click trigger
            trigger = self._find_clickable_element(selector, timeout)
            self._log_element_state(trigger, selector)
            self.scroll_to_element(trigger)
            time.sleep(0.3)

            # Click trigger
            trigger.click()

            # Wait for dropdown menu to appear
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".ant-dropdown:not(.ant-dropdown-hidden)")
                )
            )

            logger.info("   ✅ Dropdown opened successfully")

        except Exception as e:
            logger.error(f"   ❌ Failed to open dropdown: {e}")
            self._take_screenshot("dropdown_trigger_error")
            raise

    @log_method
    def click_ant_dropdown_menu_item(self, item_text: str, timeout: int = 10) -> None:
        """
        Click an item in an open Ant Design dropdown menu by text.

        Args:
            item_text: Text of the menu item to click
            timeout: Timeout in seconds
        """
        logger.info(f"📋 Clicking dropdown menu item: {item_text}")

        try:
            # Wait for dropdown menu to be visible
            dropdown_menu = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".ant-dropdown:not(.ant-dropdown-hidden)")
                )
            )

            # Build XPath selector for menu item containing text
            xpath = f"//li[contains(@class, 'ant-dropdown-menu-item')]//*[contains(text(), '{item_text}')]"

            # Wait for menu item to be clickable
            menu_item = WebDriverWait(dropdown_menu, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )

            self._log_element_state(menu_item, xpath)

            # Click the menu item
            menu_item.click()
            logger.info(f"   ✅ Menu item '{item_text}' clicked")

            # Wait for dropdown to close
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, ".ant-dropdown:not(.ant-dropdown-hidden)")
                )
            )

        except Exception as e:
            logger.error(f"   ❌ Failed to click menu item: {e}")
            self._take_screenshot("dropdown_menu_item_error")
            raise

    @log_method
    def ant_select_option(self, dropdown_selector: str, option_text: str, timeout: int = 30) -> None:
        """
        Ant Design Select handler - for custom div-based dropdowns.
        Do NOT use for native <select> elements.

        Args:
            dropdown_selector: Selector for the dropdown trigger element
            option_text: Text of the option to select
            timeout: Timeout in seconds
        """
        logger.info(f"📋 Ant Design Select: {dropdown_selector}, Option: {option_text}")

        try:
            # Wait for loading to finish
            logger.info("📋 Waiting for dropdown to finish loading...")
            try:
                loading_indicator = self.driver.find_element(By.CSS_SELECTOR, ".ant-select-loading")
                WebDriverWait(self.driver, 15).until(EC.invisibility_of_element(loading_indicator))
                logger.info("✅ Dropdown finished loading")
            except:
                logger.info("ℹ️ No loading state detected")

            # Click to open dropdown
            logger.info(f"📋 Opening dropdown: {dropdown_selector}")
            self.click_element(dropdown_selector, timeout)

            # Wait for dropdown panel to be visible
            dropdown_panel = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".ant-select-dropdown:not(.ant-select-dropdown-hidden)"))
            )
            logger.info("✅ Dropdown panel visible")

            # Try to find and click the option
            option_xpath = f"//div[contains(@class, 'ant-select-item-option') and @title='{option_text}']"

            try:
                option = WebDriverWait(dropdown_panel, 5).until(
                    EC.element_to_be_clickable((By.XPATH, option_xpath))
                )
                option.click()
                logger.info(f"✅ Selected: {option_text}")

                # Wait for dropdown to close
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element(
                        (By.CSS_SELECTOR, ".ant-select-dropdown:not(.ant-select-dropdown-hidden)"))
                )
                return
            except TimeoutException:
                # Option not immediately visible, might be in virtual list
                logger.info("📜 Option not immediately visible, scrolling virtual list...")

                # Scroll through virtual list
                virtual_list = dropdown_panel.find_element(By.CSS_SELECTOR, ".rc-virtual-list-holder")

                for attempt in range(30):
                    try:
                        option = self.driver.find_element(By.XPATH, option_xpath)
                        if option.is_displayed():
                            option.click()
                            logger.info(f"✅ Selected: {option_text} (after {attempt} scrolls)")
                            WebDriverWait(self.driver, 5).until(
                                EC.invisibility_of_element(
                                    (By.CSS_SELECTOR, ".ant-select-dropdown:not(.ant-select-dropdown-hidden)"))
                            )
                            return
                    except (NoSuchElementException, ElementNotInteractableException):
                        pass

                    # Scroll down in virtual list
                    self.driver.execute_script("arguments[0].scrollTop += 100", virtual_list)
                    time.sleep(0.1)

                raise TimeoutException(f"Could not find option '{option_text}' after scrolling")

        except Exception as e:
            logger.error(f"   ❌ Ant Design Select failed: {e}")
            self._take_screenshot("ant_select_error")
            raise

    @log_method
    def ant_select_date_picker(self, selector: str, date_value: str, timeout: int = 30) -> None:
        """
        Fill in an Ant Design date picker.

        Args:
            selector: Selector for the date input
            date_value: Date string to enter
            timeout: Timeout in seconds
        """
        logger.info(f"📅 Date Picker: {selector}, Date: {date_value}")
        element = self._find_element(selector, timeout)
        element.clear()
        element.send_keys(date_value)
        element.send_keys(Keys.ENTER)  # Confirm date selection

    # --- Text and Attribute Retrieval ---

    @log_method
    def get_text(self, selector: str, timeout: int = 30) -> str:
        """Get the visible text of an element."""
        logger.info(f"📝 Getting text from: {selector}")
        element = self._find_element(selector, timeout)
        text = element.text
        logger.info(f"   Text: '{text}'")
        return text

    @log_method
    def get_attribute(self, selector: str, attribute: str, timeout: int = 30) -> str:
        """Get an attribute value from an element."""
        logger.info(f"🔍 Getting attribute '{attribute}' from: {selector}")
        element = self._find_element(selector, timeout)
        value = element.get_attribute(attribute)
        logger.info(f"   Value: '{value}'")
        return value

    @log_method
    def get_value(self, selector: str, timeout: int = 30) -> str:
        """Get the value attribute of an input element."""
        return self.get_attribute(selector, 'value', timeout)

    def get_value_from_selector(self, selector: str, timeout: int = 30) -> str:
        """Alias for get_text."""
        return self.get_text(selector, timeout)

    # --- Element State Verification ---

    @log_method
    def verify_element_visible(self, selector: str, timeout: int = 30) -> None:
        """Verify that an element is visible."""
        logger.info(f"👁️ Verifying visibility: {selector}")
        by, value = self._get_by_strategy(selector)
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            logger.info(f"   ✅ Element is visible")
        except TimeoutException:
            logger.error(f"   ❌ Element not visible within {timeout}s")
            self._take_screenshot("element_not_visible")
            raise AssertionError(f"Element '{selector}' is not visible")

    @log_method
    def verify_element_not_visible(self, selector: str, timeout: int = 5) -> None:
        """Verify that an element is not visible or doesn't exist."""
        logger.info(f"👁️ Verifying NOT visible: {selector}")
        by, value = self._get_by_strategy(selector)
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by, value))
            )
            logger.info(f"   ✅ Element is not visible")
        except TimeoutException:
            logger.error(f"   ❌ Element is still visible after {timeout}s")
            raise AssertionError(f"Element '{selector}' is still visible")

    @log_method
    def verify_text_visible(self, text: str, timeout: int = 30) -> None:
        """Verify that text is visible on the page."""
        logger.info(f"📝 Verifying text visible: {text}")
        xpath = f"//*[contains(text(), '{text}')]"
        try:
            self.verify_element_visible(xpath, timeout)
        except AssertionError:
            raise AssertionError(f"Text '{text}' is not visible on page")

    @log_method
    def verify_has_text_visible(self, selector: str, expected_text: str, timeout: int = 30) -> None:
        """Verify that an element contains specific text."""
        logger.info(f"📝 Verifying element has text: {selector} -> '{expected_text}'")
        element = self._find_element(selector, timeout)
        actual_text = element.text

        if expected_text not in actual_text:
            logger.error(f"   ❌ Text mismatch: expected '{expected_text}', found '{actual_text}'")
            raise AssertionError(f"Element text '{actual_text}' does not contain '{expected_text}'")

        logger.info(f"   ✅ Text verified")

    @log_method
    def verify_url_contains(self, expected_substring: str, timeout: int = 30) -> None:
        """Verify that current URL contains expected substring."""
        logger.info(f"🌐 Verifying URL contains: {expected_substring}")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(expected_substring)
            )
            logger.info(f"   ✅ URL verified: {self.driver.current_url}")
        except TimeoutException:
            current_url = self.driver.current_url
            logger.error(f"   ❌ URL verification failed: {current_url}")
            raise AssertionError(f"URL '{current_url}' does not contain '{expected_substring}'")

    @log_method
    def verify_title(self, expected_title: str, timeout: int = 30) -> None:
        """Verify page title."""
        logger.info(f"📄 Verifying title: {expected_title}")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.title_is(expected_title)
            )
            logger.info(f"   ✅ Title verified")
        except TimeoutException:
            actual_title = self.driver.title
            logger.error(f"   ❌ Title mismatch: expected '{expected_title}', got '{actual_title}'")
            raise AssertionError(f"Title mismatch: expected '{expected_title}', got '{actual_title}'")

    @log_method
    def verify_title_contains(self, expected_substring: str, timeout: int = 30) -> None:
        """Verify page title contains substring."""
        logger.info(f"📄 Verifying title contains: {expected_substring}")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.title_contains(expected_substring)
            )
            logger.info(f"   ✅ Title verified: {self.driver.title}")
        except TimeoutException:
            actual_title = self.driver.title
            logger.error(f"   ❌ Title verification failed: {actual_title}")
            raise AssertionError(f"Title '{actual_title}' does not contain '{expected_substring}'")

    # --- Validation Error Handling ---

    @log_method
    def verify_validation_error(self, error_text: str, timeout: int = 30) -> None:
        """Verify validation error message is displayed."""
        logger.info(f"⚠️ Verifying validation error: {error_text}")
        self.verify_text_visible(error_text, timeout)

    def verify_field_error_by_text(self, error_text: str) -> None:
        """Verify field validation error by text content."""
        logger.info(f"⚠️ Verifying field error: {error_text}")
        self.verify_text_visible(error_text)

    def get_validation_error_text(self, selector: str = 'p.text-xs.mt-1') -> str:
        """Get validation error text from error paragraph."""
        return self.get_value_from_selector(selector)

    @log_method
    def is_validation_error_visible(self, error_text: str) -> bool:
        """Check if validation error with specific text is visible."""
        logger.info(f"🔍 Checking validation error visibility: {error_text}")
        xpath = f"//*[contains(text(), '{error_text}')]"
        result = self.is_visible(xpath)
        logger.info(f"   Result: {result}")
        return result

    def wait_for_validation_error(self, error_text: str, timeout: int = 5) -> WebElement:
        """Wait for validation error to appear."""
        logger.info(f"⏳ Waiting for validation error: {error_text}")
        xpath = f"//*[contains(text(), '{error_text}')]"
        return self._find_element(xpath, timeout)

    # --- Waiting ---

    @log_method
    def wait_for_selector(self, selector: str, state: str = "visible", timeout: int = 30) -> WebElement:
        """
        Wait for a selector to reach the specified state.

        Args:
            selector: Element selector
            state: State to wait for ('visible', 'present', 'clickable', 'invisible')
            timeout: Timeout in seconds
        """
        logger.info(f"⏳ Waiting for: {selector}, State: {state}")
        by, value = self._get_by_strategy(selector)
        wait = WebDriverWait(self.driver, timeout)

        if state == "visible":
            element = wait.until(EC.visibility_of_element_located((by, value)))
        elif state == "present":
            element = wait.until(EC.presence_of_element_located((by, value)))
        elif state == "clickable":
            element = wait.until(EC.element_to_be_clickable((by, value)))
        elif state == "invisible":
            wait.until(EC.invisibility_of_element_located((by, value)))
            return None
        else:
            raise ValueError(f"Invalid state: {state}")

        return element

    @log_method
    def wait_for_url(self, url: str, timeout: int = 30) -> None:
        """Wait for navigation to a URL."""
        logger.info(f"⏳ Waiting for URL: {url}")
        WebDriverWait(self.driver, timeout).until(EC.url_to_be(url))

    @log_method
    def wait_for_url_contains(self, url_substring: str, timeout: int = 30) -> None:
        """Wait for URL to contain substring."""
        logger.info(f"⏳ Waiting for URL to contain: {url_substring}")
        WebDriverWait(self.driver, timeout).until(EC.url_contains(url_substring))

    def wait(self, seconds: float) -> None:
        """Wait for a specified duration (use sparingly)."""
        logger.info(f"⏱️ Waiting for {seconds}s")
        time.sleep(seconds)

    # --- Scrolling ---

    def scroll_to_element(self, element: WebElement) -> None:
        """Scroll element into view."""
        logger.info("📜 Scrolling to element")
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(0.5)  # Give time for smooth scroll

    def scroll_to_element_by_selector(self, selector: str) -> None:
        """Scroll to an element identified by selector."""
        logger.info(f"📜 Scrolling to: {selector}")
        element = self._find_element(selector)
        self.scroll_to_element(element)

    def scroll_down(self, pixels: int = None) -> None:
        """Scroll down the page."""
        if pixels:
            logger.info(f"📜 Scrolling down {pixels}px")
            self.driver.execute_script(f"window.scrollBy(0, {pixels})")
        else:
            logger.info("📜 Scrolling to bottom")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self) -> None:
        """Scroll to the top of the page."""
        logger.info("📜 Scrolling to top")
        self.driver.execute_script("window.scrollTo(0, 0)")

    # --- Screenshots ---

    def screenshot(self, filepath: str) -> None:
        """Take a screenshot of the page."""
        logger.info(f"📸 Taking screenshot: {filepath}")
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        self.driver.save_screenshot(filepath)

    def screenshot_element(self, selector: str, filepath: str) -> None:
        """Take a screenshot of a specific element."""
        logger.info(f"📸 Taking element screenshot: {selector} -> {filepath}")
        element = self._find_element(selector)
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        element.screenshot(filepath)

    # --- JavaScript Execution ---

    def evaluate(self, script: str, *args):
        """Execute JavaScript in the page context."""
        logger.info(f"⚙️ Evaluating JS: {script[:50]}...")
        return self.driver.execute_script(script, *args)

    # --- State Checks ---

    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        try:
            element = self._find_element(selector, timeout=2)
            result = element.is_displayed()
            logger.debug(f"👁️ Is visible '{selector}': {result}")
            return result
        except (TimeoutException, NoSuchElementException):
            logger.debug(f"👁️ Is visible '{selector}': False")
            return False

    def is_enabled(self, selector: str) -> bool:
        """Check if an element is enabled."""
        try:
            element = self._find_element(selector, timeout=2)
            result = element.is_enabled()
            logger.debug(f"✅ Is enabled '{selector}': {result}")
            return result
        except (TimeoutException, NoSuchElementException):
            logger.debug(f"✅ Is enabled '{selector}': False")
            return False

    def is_checked(self, selector: str) -> bool:
        """Check if a checkbox/radio is checked."""
        try:
            element = self._find_element(selector, timeout=2)
            result = element.is_selected()
            logger.debug(f"☑️ Is checked '{selector}': {result}")
            return result
        except (TimeoutException, NoSuchElementException):
            logger.debug(f"☑️ Is checked '{selector}': False")
            return False

    def count_elements(self, selector: str) -> int:
        """Count the number of elements matching the selector."""
        try:
            elements = self._find_elements(selector, timeout=2)
            count = len(elements)
            logger.debug(f"🔢 Count '{selector}': {count}")
            return count
        except (TimeoutException, NoSuchElementException):
            logger.debug(f"🔢 Count '{selector}': 0")
            return 0

    def element_exists(self, selector: str) -> bool:
        """Check if an element exists in the DOM."""
        try:
            self._find_element(selector, timeout=2)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    # --- Helper Methods for Logging ---

    def _log_element_state(self, element: WebElement, selector: str):
        """Log detailed element state information."""
        try:
            is_displayed = element.is_displayed()
            is_enabled = element.is_enabled()
            logger.info(f"   🔍 Element state - Displayed: {is_displayed}, Enabled: {is_enabled}")

            # Try to get text content
            try:
                text = element.text
                if text and text.strip():
                    logger.info(f"      Text: '{text.strip()[:50]}'")
            except:
                pass

        except Exception as e:
            logger.warning(f"   ⚠️ Could not log element state: {e}")

    def _take_screenshot(self, name: str):
        """Take screenshot for debugging."""
        try:
            timestamp = int(time.time())
            filename = f"screenshots/{name}_{timestamp}.png"

            # Create screenshots directory if it doesn't exist
            os.makedirs("screenshots", exist_ok=True)

            self.driver.save_screenshot(filename)
            logger.info(f"   📸 Screenshot saved: {filename}")
        except Exception as e:
            logger.warning(f"   ⚠️ Screenshot failed: {e}")

    # --- Browser Actions ---

    def switch_to_frame(self, frame_reference) -> None:
        """Switch to an iframe or frame."""
        logger.info(f"🖼️ Switching to frame: {frame_reference}")
        self.driver.switch_to.frame(frame_reference)

    def switch_to_default_content(self) -> None:
        """Switch back to the main document."""
        logger.info("🖼️ Switching to default content")
        self.driver.switch_to.default_content()

    def switch_to_window(self, window_handle: str) -> None:
        """Switch to a different window."""
        logger.info(f"🪟 Switching to window: {window_handle}")
        self.driver.switch_to.window(window_handle)

    def get_window_handles(self) -> List[str]:
        """Get all window handles."""
        return self.driver.window_handles

    def accept_alert(self) -> None:
        """Accept a JavaScript alert."""
        logger.info("⚠️ Accepting alert")
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()

    def dismiss_alert(self) -> None:
        """Dismiss a JavaScript alert."""
        logger.info("⚠️ Dismissing alert")
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.dismiss()

    def get_alert_text(self) -> str:
        """Get text from a JavaScript alert."""
        logger.info("⚠️ Getting alert text")
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        return alert.text
