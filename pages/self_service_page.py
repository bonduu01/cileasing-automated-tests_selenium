"""
Self Service Page Object
"""

import logging
from selenium.webdriver.remote.webdriver import WebDriver

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
        """Verify that the self-service page has loaded."""
        logger.info("✅ Verifying self-service page loaded")

        # Log the current URL
        current_url = self.driver.current_url
        logger.info(f"Current page URL: {current_url}")

        self.verify_element_visible(SELF_SERVICE_PAGE.PERSONAL_NAME)
        logger.info("✅ Self-service page URL verified")

    @log_method
    def click_to_logout(self) -> None:
        """Click logout button."""
        logger.info("🚪 Clicking logout")
        # Click on profile avatar first
        self.click_element_by_text("MM")
        # Then click logout link
        self.click_element_by_text("Logout")
        logger.info("✅ Logged out successfully")

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
