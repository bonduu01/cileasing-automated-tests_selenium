"""Edit Self Service Page Object"""
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from utils.constants import EDIT_SELF_SERVICE_PAGE
from utils.decorators import log_method
from config import settings

logger = logging.getLogger(__name__)


class EditSelfServicePage(BasePage):
    """Page Object for Edit Self Service Page."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        logger.info("🏗️ Initialized EditSelfServicePage")

    @log_method
    def enter_other_name(self, other_name: str) -> None:
        """Enter other name."""
        other_name = other_name or settings.other_name
        logger.info(f"📝 Entering other name: {other_name}")
        self.fill_input(EDIT_SELF_SERVICE_PAGE.OTHER_NAME, other_name)

    @log_method
    def enter_job_title(self, job_title: str) -> None:
        """Enter job title."""
        logger.info(f"💼 Entering job title: {job_title}")
        self.fill_input(EDIT_SELF_SERVICE_PAGE.JOB_TITLE, job_title)

    @log_method
    def click_submit_button(self) -> None:
        """Click submit button."""
        logger.info("✅ Clicking submit")
        self.click_element_by_text(EDIT_SELF_SERVICE_PAGE.EDIT_SUBMIT_BUTTON)
