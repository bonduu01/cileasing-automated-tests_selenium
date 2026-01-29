"""
Page selectors and UI constants.
Credentials and URLs should be loaded from .env via config/settings.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class HomePageSelectors:
    """Selectors for the Home Page."""
    TITLE: str = "CAndILeasing"


@dataclass(frozen=True)
class LoginPageSelectors:
    """Selectors for the Login Page."""
    EMAIL_INPUT: str = 'input[name="email"]'
    PASSWORD_INPUT: str = 'input[name="password"]'
    SUBMIT_BUTTON: str = 'button[type="submit"][buttontype="primary"]'
    PASSWORD_DISABLED: str = "input[name='password'][type='password']"
    # DEFAULT_COMPANY: str = 'div.space-y-4 div.uppercase:text-is("DEFAULT")'
    DEFAULT_COMPANY: str = "div.uppercase:has-text('DEFAULT')"
    FLOUR_MILLS_COMPANY: str = 'div.space-y-4 div.uppercase:text-is("FLOUR MILLS NIGERIA LIMITED GOLDEN NOODLES & PASTA IGANMU")'
    ERROR_TOAST: str = 'div[role="alert"]'
    PASSWORD_BLANK_ERROR = 'p.text-xs.mt-1:has-text("Password cannot be blank")'
    VALIDATION_ERROR = 'p.text-xs.mt-1'
    ERROR_PASSWORD_BLANK = "Password cannot be blank"
    ERROR_USERNAME_BLANK = "Email cannot be blank"
    ERROR_INVALID_CREDENTIALS = "Invalid username or password"
    DEFAULT_LINK: str = 'text="DEFAULT"'


@dataclass(frozen=True)
class SelfServicePageSelectors:
    """Selectors for the Self-Service Page."""
    PERSONAL_NAME: str = "span.text-dark0b.font-\\[400\\].text-\\[14px\\]"
    MM_PROFILE: str = "span.ant-avatar-string:has-text('MM')"
    LOGOUT_LINK: str = "p.text-danger:has-text('Logout')"
    EDIT_LINK: str = "button:has-text('Edit')"
    EDIT_SUBMIT_BUTTON: str = "button:has-text('Submit')"
    CLICK_BANK_DETAIL: str = "button:has-text('Bank Details')"
    ADD_NEW_BANK_DETAIL_BUTTON: str = "button.px-4.py-1.text-\\[\\#4F5E71\\].bg-white.border-\\[1px\\]"
    EDIT_BANK_BUTTON: str = "button:has(svg path[stroke='#5141A4'])"
    EMERGENCY_CONTACTS_BUTTON = "role=button[name='Emergency Contacts']"
    EMERGENCY_CONTACTS_ADD_BUTTON = "button[type='button']:has-text('Add New')"
    EMERGENCY_CONTACTS_EDIT_BUTTON = "div.flex.items-center:has(svg) >> text=Edit"
    BVN_BUTTON: str = 'button:has-text("BVN")'
    ADD_BVN_BUTTON: str = 'button[type="button"]:has-text("Add New")'
    EDIT_BVN_BUTTON: str = "button:has(svg path[d^='M7.3335'])"
    IDENTITY_BUTTON: str = "button:has-text('Identity')"
    CLICK_IDENTITY_ADD_BUTTON: str = "button:has-text('Add New')"


@dataclass(frozen=True)
class EditSelfServicePageSelectors:
    """Selectors for the Edit Personnel Self-Service Page."""
    OTHER_NAME: str = "input[name='otherName']"
    JOB_TITLE: str = 'input[name="jobTitle"]'
    EDIT_SUBMIT_BUTTON: str = "button:has-text('Submit')"

@dataclass(frozen=True)
class AddBankDetailsPageSelectors:
    """Selectors for the Add bank Details Self-Service Page."""
    BANK_NAME_DROPDOWN = ".ant-select-selector"
    BANK_NAME: str = "GLOBUS BANK"
    BANK_ID: str = 'input[name="financialInstitutionId"]'
    SORT_CODE: str = "input[name='sortingCode']"
    ADD_BANK_BUTTON: str = "button:has-text('Add Bank')"

@dataclass(frozen=True)
class EditBankDetailsPageSelectors:
    """Selectors for the Edit bank Details Self-Service Page."""
    BANK_NAME_DROPDOWN = ".ant-select-selector"
    BANK_NAME: str = "GLOBUS BANK"
    BANK_ID: str = 'input[name="financialInstitutionId"]'
    SORT_CODE: str = "input[name='sortingCode']"
    EDIT_SUBMIT_BUTTON: str = "button:has-text('Save Changes')"


@dataclass(frozen=True)
class AddEmergencyContactPageSelectors:
    FIRST_NAME: str = 'input[name="firstName"]'
    VERIFY_FIRST_NAME: str = 'text="First Name cannot be blank"'
    OTHER_NAME: str = 'input[name="otherName"]'
    SURNAME: str = 'input[name="surname"]'
    VERIFY_SURNAME: str = "text=Surname cannot be blank"
    MAIDEN_NAME: str = "input[name='maidenName']"
    PREVIOUS_NAME: str = "input[name='previousName']"
    MOBILE_NUMBER: str = "input[name='mobileNumber']"
    WORK_NUMBER: str = "input[name='workNumber']"
    RELATIONSHIP: str = "input[name='relationship']"
    EMAIL: str = "input[name='email']"
    LOCATION: str = "input[name='location']"
    ADD_CONTACT_BUTTON: str = "button:has-text('Add Contact')"


@dataclass(frozen=True)
class EditEmergencyContactPageSelectors:
    FIRST_NAME: str = 'input[name="firstName"]'
    OTHER_NAME: str = 'input[name="otherName"]'
    SURNAME: str = 'input[name="surname"]'
    MAIDEN_NAME: str = "input[name='maidenName']"
    PREVIOUS_NAME: str = "input[name='previousName']"
    MOBILE_NUMBER: str = "input[name='mobileNumber']"
    WORK_NUMBER: str = "input[name='workNumber']"
    RELATIONSHIP: str = "input[name='relationship']"
    EMAIL: str = "input[name='email']"
    LOCATION: str = "input[name='location']"
    EDIT_CONTACT_BUTTON: str = "role=button[name='Save Changes']"


@dataclass(frozen=True)
class AddBnvPageSelectors:
    """Selectors for Add BVN Self-Service Page."""
    BVN_INPUT: str = 'input[name="bvn"]'
    ADD_BVN_BUTTON: str = "button[type='submit']:has-text('Add BVN')"


@dataclass(frozen=True)
class EditBnvPageSelectors:
    """Selectors for Add BVN Self-Service Page."""
    EDIT_INPUT: str = 'input[name="bvn"]'
    EDIT_BVN_BUTTON: str = 'button[type="submit"]:has-text("Save Changes")'


@dataclass(frozen=True)
class AddIdentityPageSelectors:
    """Selectors for the Add bank Details Self-Service Page."""
    IDENTITY_TYPE_DROPDOWN = ".ant-select-selector"
    IDENTITY_TYPE: str = "DRIVERS LICENSE"
    IDENTITY_ID: str = 'input[name="identityId"]'
    ISSUED_DATE_SELECTOR: str = 'label:has-text("Issued Date") + div.ant-picker input'
    EXPIRY_DATE_SELECTOR: str = 'label:has-text("Expiry Date") + div.ant-picker input'
    ADD_IDENTITY_BUTTON: str = 'button:has-text("Add")'

# Create singleton instances
HOME_PAGE = HomePageSelectors()
LOGIN_PAGE = LoginPageSelectors()
SELF_SERVICE_PAGE = SelfServicePageSelectors()
EDIT_SELF_SERVICE_PAGE = EditSelfServicePageSelectors()
ADD_BANK_DETAILS_PAGE = AddBankDetailsPageSelectors()
EDIT_BANK_DETAILS_PAGE = EditBankDetailsPageSelectors()
ADD_EMERGENCY_CONTACT_PAGE = AddEmergencyContactPageSelectors()
EDIT_EMERGENCY_CONTACT_PAGE = EditEmergencyContactPageSelectors()
ADD_BVN_PAGE = AddBnvPageSelectors()
EDIT_BVN_PAGE = EditBnvPageSelectors()
ADD_IDENTITY_PAGE = AddIdentityPageSelectors()
