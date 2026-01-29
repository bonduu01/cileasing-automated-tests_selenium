"""
Page Objects package for the Selenium test framework.
"""

from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.self_service_page import SelfServicePage
from pages.edit_self_service_page import EditSelfServicePage
from pages.add_bank_details_page import AddBankDetailsPage
from pages.edit_bank_details_page import EditBankDetailsPage
from pages.add_emergency_contact_page import AddEmergencyContactPage
from pages.edit_emergency_contact_page import EditEmergencyContactPage
from pages.add_bvn_page import AddBvnPage
from pages.edit_bvn_page import EditBvnPage
from pages.add_identity_page import AddIdentityPage

__all__ = [
    "BasePage",
    "HomePage",
    "LoginPage",
    "SelfServicePage",
    "EditSelfServicePage",
    "AddBankDetailsPage",
    "EditBankDetailsPage",
    "AddEmergencyContactPage",
    "EditEmergencyContactPage",
    "AddBvnPage",
    "EditBvnPage",
    "AddIdentityPage",
]
