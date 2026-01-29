"""
Application settings loaded from environment variables.
Uses pydantic-settings for type-safe configuration management.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with automatic .env file loading."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application URLs
    base_url: str = "https://candileasing.netlify.app/"
    login_url: str = ""
    self_service_url: str = ""
    edit_self_service_url: str = ""
    add_bank_details_url: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        # Set default URLs based on base_url if not provided
        if not self.login_url:
            self.login_url = self.base_url
        if not self.self_service_url:
            self.self_service_url = f"{self.base_url}personal/self-service"
        if not self.edit_self_service_url:
            self.edit_self_service_url = f"{self.base_url}personal/self-service/personal-data/edit"
        if not self.add_bank_details_url:
            self.add_bank_details_url = f"{self.base_url}personal/self-service/bank-details/add"

    # Test Credentials
    test_username: str = ""
    test_password: str = ""
    test_wrong_username: str = "bonduu001@yahoo.com"
    test_wrong_password: str = "Bat165474@@"

    # Test Data
    test_other_name: str = "OLADEJO"
    test_job_title: str = "HEAD OF IT"
    bank_name: str = "GLOBUS BANK"
    bank_id: str = "UNAFNGLA228"
    sort_code: str = "033"
    first_name: str = ""
    other_name: str = ""
    surname: str = ""
    maiden_name: str = ""
    previous_name: str = ""
    mobile_number: str = ""
    work_number: str = ""
    relationship: str = ""
    email: str = ""
    location: str = ""
    relationship_1: str = ""
    test_bvn_number: str = "22857690875"
    test_bvn_number1: str = "22857690432"
    test_identity_type: str = ""
    test_identity_id: str = ""
    test_issued_date: str = ""
    test_expiry_date: str = ""

    # Browser Settings
    browser: str = "chrome"
    headless: bool = False
    implicit_wait: int = 10
    explicit_wait: int = 30
    page_load_timeout: int = 60

    # Window Settings
    window_width: int = 1920
    window_height: int = 1080
    maximize_window: bool = True

    # Screenshot Settings
    screenshot_on_failure: bool = True
    screenshot_dir: str = "screenshots/"

    # Logging Settings
    log_level: str = "INFO"
    log_dir: str = "logs/"

    # Video Recording
    record_video: bool = False
    video_dir: str = "videos/"


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache for singleton-like behavior.
    """
    return Settings()


# Convenience export
settings = get_settings()
