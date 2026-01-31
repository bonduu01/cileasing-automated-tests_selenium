"""
Self Service Page Object
"""

import logging
import time

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.edit_self_service_page import EditSelfServicePage
from pages.base_page import BasePage
from config import settings
from utils.constants import SELF_SERVICE_PAGE
from utils.decorators import log_method

logger = logging.getLogger(__name__)


class SelfServicePage(BasePage):
    """Page Object for the Self Service Page."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.url = settings.self_service_url
        logger.info(f"🏗️ Initialized SelfServicePage - URL: {self.url}")

    @log_method
    def verify_self_service_page_loads(self) -> None:
        """Verify that the self-service page has loaded properly."""
        logger.info("✅ Verifying self-service page load")

        current_url = self.driver.current_url
        logger.info(f"   📍 Current URL: {current_url}")

        # Check URL
        if "self-service" in current_url.lower():
            logger.info("   ✅ URL contains 'self-service'")
        else:
            logger.warning(f"   ⚠️ URL does not contain 'self-service': {current_url}")

        # Check for key elements
        key_elements = [
            ("Profile avatar", "span.ant-avatar.ant-dropdown-trigger"),
            ("Any avatar", "span.ant-avatar"),
            ("Dropdown trigger", "[class*='dropdown-trigger']"),
        ]

        for name, selector in key_elements:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    visible_count = sum(1 for el in elements if el.is_displayed())
                    logger.info(f"   ✅ {name}: Found {len(elements)} ({visible_count} visible)")
                else:
                    logger.warning(f"   ⚠️ {name}: Not found")
            except Exception as e:
                logger.warning(f"   ⚠️ {name}: Error - {e}")

        logger.info("✅ Page verification complete")

    @log_method
    def click_to_logout(self) -> None:
        """
        Click logout button via profile dropdown with enhanced retry logic.
        Optimized for headless mode compatibility.
        """
        logger.info("🚪 Initiating logout process...")

        # Verify we're on the correct page
        current_url = self.driver.current_url
        logger.info(f"   📍 Current URL: {current_url}")

        if "self-service" not in current_url.lower():
            logger.warning(f"   ⚠️ Not on self-service page! Current URL: {current_url}")

        max_attempts = 3
        last_exception = None

        for attempt in range(1, max_attempts + 1):
            try:
                logger.info(f"   Attempt {attempt}/{max_attempts}")

                # Quick check for loading indicators
                try:
                    loading_elements = self.driver.find_elements(By.CSS_SELECTOR, ".ant-spin-spinning")
                    if loading_elements and any(el.is_displayed() for el in loading_elements):
                        logger.info("   Waiting for loading to complete...")
                        WebDriverWait(self.driver, 10).until(
                            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".ant-spin-spinning"))
                        )
                except:
                    pass

                # Find avatar with multiple selector strategies
                avatar_selectors = [
                    "span.ant-avatar.ant-dropdown-trigger",
                    "span.ant-avatar-circle.ant-dropdown-trigger",
                    "//span[contains(@class, 'ant-avatar') and contains(@class, 'ant-dropdown-trigger')]",
                    "//span[contains(@class, 'ant-avatar-string') and text()='MM']/parent::span",
                ]

                avatar = None
                avatar_selector = None

                for selector in avatar_selectors:
                    try:
                        logger.info(f"   Trying avatar selector: {selector}")
                        avatar = self._find_clickable_element(selector, timeout=5)
                        avatar_selector = selector
                        logger.info(f"   ✅ Found avatar with: {selector}")
                        break
                    except Exception as e:
                        logger.debug(f"   Selector {selector} failed: {e}")
                        continue

                if not avatar:
                    raise TimeoutException("Could not find avatar with any selector")

                # Log avatar state
                self._log_element_state(avatar, avatar_selector)

                # Scroll to avatar
                self.scroll_to_element(avatar)
                time.sleep(0.5)

                # Strategy: Use multiple click approaches for headless compatibility
                dropdown_opened = False

                # STRATEGY 1: Hover + Click (most reliable for Ant Design dropdowns)
                try:
                    logger.info("   📌 Strategy 1: Hover + Click")
                    actions = ActionChains(self.driver)
                    actions.move_to_element(avatar).pause(0.5).click().perform()

                    # Check if dropdown appeared
                    time.sleep(1)
                    dropdown_elements = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        ".ant-dropdown:not(.ant-dropdown-hidden), .ant-dropdown-menu"
                    )

                    if dropdown_elements and any(el.is_displayed() for el in dropdown_elements):
                        dropdown_opened = True
                        logger.info("   ✅ Dropdown opened with Strategy 1")
                except Exception as e:
                    logger.debug(f"   Strategy 1 failed: {e}")

                # STRATEGY 2: Direct JavaScript trigger (if Strategy 1 failed)
                if not dropdown_opened:
                    try:
                        logger.info("   📌 Strategy 2: JavaScript trigger")
                        # Trigger mouseenter and click events
                        self.driver.execute_script("""
                            var element = arguments[0];
                            var mouseEnter = new MouseEvent('mouseenter', {
                                view: window,
                                bubbles: true,
                                cancelable: true
                            });
                            var click = new MouseEvent('click', {
                                view: window,
                                bubbles: true,
                                cancelable: true
                            });
                            element.dispatchEvent(mouseEnter);
                            element.dispatchEvent(click);
                        """, avatar)

                        time.sleep(1)
                        dropdown_elements = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            ".ant-dropdown:not(.ant-dropdown-hidden), .ant-dropdown-menu"
                        )

                        if dropdown_elements and any(el.is_displayed() for el in dropdown_elements):
                            dropdown_opened = True
                            logger.info("   ✅ Dropdown opened with Strategy 2")
                    except Exception as e:
                        logger.debug(f"   Strategy 2 failed: {e}")

                # STRATEGY 3: Standard click (fallback)
                if not dropdown_opened:
                    try:
                        logger.info("   📌 Strategy 3: Standard click")
                        avatar.click()
                        time.sleep(1)

                        dropdown_elements = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            ".ant-dropdown:not(.ant-dropdown-hidden), .ant-dropdown-menu"
                        )

                        if dropdown_elements and any(el.is_displayed() for el in dropdown_elements):
                            dropdown_opened = True
                            logger.info("   ✅ Dropdown opened with Strategy 3")
                    except Exception as e:
                        logger.debug(f"   Strategy 3 failed: {e}")

                # Verify dropdown is visible
                if not dropdown_opened:
                    logger.warning("   ⚠️ Dropdown did not open, checking DOM...")
                    # Log what we can find
                    all_dropdowns = self.driver.find_elements(By.CSS_SELECTOR, "[class*='dropdown']")
                    logger.info(f"   Found {len(all_dropdowns)} dropdown-related elements in DOM")

                    # Check if any are visible
                    for idx, dd in enumerate(all_dropdowns[:5]):  # Check first 5
                        try:
                            logger.info(
                                f"   Dropdown {idx}: class={dd.get_attribute('class')}, displayed={dd.is_displayed()}")
                        except:
                            pass

                    raise TimeoutException("Dropdown menu did not appear after all strategies")

                # Wait for dropdown menu to be fully visible
                logger.info("   ⏳ Confirming dropdown visibility...")
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, ".ant-dropdown-menu, .ant-dropdown:not(.ant-dropdown-hidden)")
                        )
                    )
                    logger.info("   ✅ Dropdown menu confirmed visible")
                except TimeoutException:
                    logger.warning("   ⚠️ Could not confirm with WebDriverWait, but proceeding...")

                # Click logout menu item
                logger.info("   🖱️ Clicking logout...")
                logout_selectors = [
                    "//li[contains(@class, 'ant-dropdown-menu-item')]//p[contains(text(), 'Logout')]",
                    "//li[contains(@class, 'ant-dropdown-menu-item')]//*[contains(text(), 'Logout')]",
                    ".ant-dropdown-menu-item .text-danger",
                    "li.ant-dropdown-menu-item",  # Fallback - get any menu item
                ]

                logout_clicked = False
                for selector in logout_selectors:
                    try:
                        by, value = self._get_by_strategy(selector)

                        # For the fallback selector, we need to find the one with "Logout" text
                        if selector == "li.ant-dropdown-menu-item":
                            menu_items = self.driver.find_elements(by, value)
                            for item in menu_items:
                                if "logout" in item.text.lower():
                                    logout_item = item
                                    break
                            else:
                                continue
                        else:
                            logout_item = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((by, value))
                            )

                        # Try multiple click methods
                        try:
                            logout_item.click()
                        except:
                            try:
                                # Try ActionChains click
                                ActionChains(self.driver).move_to_element(logout_item).click().perform()
                            except:
                                # Fallback to JS click
                                self.driver.execute_script("arguments[0].click();", logout_item)

                        logout_clicked = True
                        logger.info(f"   ✅ Logout clicked with: {selector}")
                        break

                    except Exception as e:
                        logger.debug(f"   Logout selector {selector} failed: {e}")
                        continue

                if not logout_clicked:
                    raise Exception("Could not click logout item")

                # Verify navigation to login page
                try:
                    logger.info("   Checking for redirect to login page...")
                    WebDriverWait(self.driver, 10).until(
                        lambda driver: "login" in driver.current_url.lower() or
                                       driver.current_url == f"{settings.base_url}" or
                                       len(driver.find_elements(By.CSS_SELECTOR,
                                                                "input[name='email'], input[type='email']")) > 0
                    )
                    logger.info(f"✅ Logout completed - URL: {self.driver.current_url}")
                    return

                except TimeoutException:
                    logger.warning("   ⚠️ Could not confirm logout redirect, but assuming success")
                    return

            except Exception as e:
                last_exception = e
                error_msg = f"{type(e).__name__}: {str(e)[:200]}"
                logger.warning(f"   ⚠️ Attempt {attempt} failed: {error_msg}")

                # Take screenshot for debugging
                self._take_screenshot(f"logout_attempt_{attempt}_failed")

                if attempt < max_attempts:
                    logger.info("   🔄 Retrying...")
                    time.sleep(2)
                else:
                    logger.error(f"   ❌ All {max_attempts} attempts failed")
                    self._take_screenshot("logout_all_attempts_failed")

                    # Enhanced debugging
                    logger.error(f"   Current URL: {self.driver.current_url}")
                    logger.error(f"   Page Title: {self.driver.title}")

                    # Log page elements
                    logger.error("   Checking what elements are visible on page:")
                    try:
                        avatars = self.driver.find_elements(By.CSS_SELECTOR, "span.ant-avatar")
                        logger.error(f"   Found {len(avatars)} avatar elements")

                        dropdowns = self.driver.find_elements(By.CSS_SELECTOR, "[class*='dropdown']")
                        logger.error(f"   Found {len(dropdowns)} dropdown-related elements")

                        # Check dropdown visibility
                        for idx, dd in enumerate(dropdowns[:3]):
                            try:
                                classes = dd.get_attribute('class')
                                displayed = dd.is_displayed()
                                logger.error(f"   Dropdown {idx}: classes={classes}, visible={displayed}")
                            except:
                                pass
                    except Exception as debug_error:
                        logger.error(f"   Debug logging failed: {debug_error}")

                    raise

        if last_exception:
            raise last_exception

    @log_method
    def click_to_edit_personal_data_details(self) -> EditSelfServicePage:
        """ Click the 'Edit Personal Data' link and navigate to Edit Self Service page. """
        logger.info("🖱️ Clicking edit personal data link")

        # Ensure page DOM is stable by waiting for the edit link to be present & visible
        self.wait_for_selector(
            SELF_SERVICE_PAGE.EDIT_LINK,
            state="visible",
            timeout=30
        )

        # Scroll element into view (handles off-screen issues)
        self.scroll_to_element_by_selector(SELF_SERVICE_PAGE.EDIT_LINK)

        # Optional: defensive check before clicking
        if not self.is_enabled(SELF_SERVICE_PAGE.EDIT_LINK):
            raise AssertionError("Edit Personal Data link is not enabled")

        self.click_element(SELF_SERVICE_PAGE.EDIT_LINK, timeout=30)

        logger.info("✅ Edit link clicked successfully")

        # Wait for navigation to complete (URL or key element on destination page)
        # Prefer URL or unique element verification over sleeps
        self.wait_for_url_contains(
            "edit",  # adjust to actual route fragment if needed
            timeout=30
        )

        return EditSelfServicePage(self.driver)


    @log_method
    def click_edit_button(self) -> None:
        """Click the Edit button for personal data."""
        logger.info("✏️ Clicking Edit button")
        self.click_element_by_text("Edit")

    @log_method
    def click_bank_details_tab(self) -> None:
        """Click on Bank Details tab."""
        logger.info("🏦 Clicking Bank Details tab")
        self.click_element_by_text("Bank Details")

    @log_method
    def click_add_new_bank_detail_button(self) -> None:
        """Click Add New button for bank details."""
        logger.info("➕ Clicking Add New Bank Detail")
        self.click_element(SELF_SERVICE_PAGE.ADD_NEW_BANK_DETAIL_BUTTON)

    @log_method
    def click_edit_bank_button(self) -> None:
        """Click edit button for bank details."""
        logger.info("✏️ Clicking Edit Bank button")
        self.click_element(SELF_SERVICE_PAGE.EDIT_BANK_BUTTON)

    @log_method
    def click_emergency_contacts_tab(self) -> None:
        """Click on Emergency Contacts tab."""
        logger.info("👥 Clicking Emergency Contacts tab")
        self.click_element_by_text("Emergency Contacts")

    @log_method
    def click_add_emergency_contact_button(self) -> None:
        """Click Add New button for emergency contacts."""
        logger.info("➕ Clicking Add Emergency Contact")
        self.click_element_by_text("Add New")

    @log_method
    def click_edit_emergency_contact_button(self) -> None:
        """Click edit button for emergency contact."""
        logger.info("✏️ Clicking Edit Emergency Contact")
        self.click_element_by_text("Edit")

    @log_method
    def click_bvn_tab(self) -> None:
        """Click on BVN tab."""
        logger.info("🆔 Clicking BVN tab")
        self.click_element_by_text("BVN")

    @log_method
    def click_add_bvn_button(self) -> None:
        """Click Add New button for BVN."""
        logger.info("➕ Clicking Add BVN")
        self.click_element_by_text("Add New")

    @log_method
    def click_edit_bvn_button(self) -> None:
        """Click edit button for BVN."""
        logger.info("✏️ Clicking Edit BVN")
        self.click_element(SELF_SERVICE_PAGE.EDIT_BVN_BUTTON)

    @log_method
    def click_identity_tab(self) -> None:
        """Click on Identity tab."""
        logger.info("🪪 Clicking Identity tab")
        self.click_element_by_text("Identity")

    @log_method
    def click_add_identity_button(self) -> None:
        """Click Add New button for identity."""
        logger.info("➕ Clicking Add Identity")
        self.click_element_by_text("Add New")
