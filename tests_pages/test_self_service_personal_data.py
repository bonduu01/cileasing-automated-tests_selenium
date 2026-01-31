# import pytest
# from pages import SelfServicePage, EditSelfServicePage
# from config import settings
# import logging
# from selenium.webdriver.remote.webdriver import WebDriver
#
# logger = logging.getLogger(__name__)
#
#
# class TestEditSelfServicePage:
#     """Test suite for Self-Service functionalities."""
#
#
#     @pytest.fixture(autouse=True)
#     def setup(self, authenticated_driver: WebDriver):
#         """Setup method that runs before each test."""
#         logger.info("🔧 Setting up test fixtures")
#         self.driver = authenticated_driver
#         self.self_service_page = SelfServicePage(self.driver)
#         self.edit_self_service_page = EditSelfServicePage(self.driver)
#
#         logger.info("✅ Setup complete")
#         # Cleanup if needed
#
#     @pytest.mark.regression
#     def test_edit_personal_details(self) -> None:
#         """Test editing personal details."""
#         logger.info("📝 Starting test: Edit Personal Details")
#
#         # Navigate to edit page
#         logger.info("🔄 Navigating to edit personal data page")
#         self.self_service_page.click_to_edit_personal_data_details()
#
#         # Fill in the form
#         logger.info("📝 Filling in personal details")
#         self.edit_self_service_page.enter_other_name("TestOtherName")
#         self.edit_self_service_page.enter_job_title("Test Job Title")
#
#         # Submit the form
#         logger.info("✅ Submitting form")
#         self.edit_self_service_page.click_submit_button()
#
#         # Add assertions here as needed
#         logger.info("✅ Test completed successfully")
#
