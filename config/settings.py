"""
Enhanced Configuration Management using Pydantic Settings
Loads configuration from .env file with validation
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator
from pathlib import Path
from typing import Literal, Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ==================== URLs ====================
    base_url: str = Field(default="https://candileasing.netlify.app", description="Base application URL")
    login_url: str = Field(default="https://candileasing.netlify.app", description="Login page URL")
    api_url: Optional[str] = Field(default=None, description="API base URL")

    # ==================== Credentials ====================
    valid_username: str = Field(default="student", description="Valid test username")
    valid_password: str = Field(default="Password123", description="Valid test password")
    admin_username: Optional[str] = Field(default="admin", description="Admin username")
    admin_password: Optional[str] = Field(default="Admin123!", description="Admin password")

    # ==================== Browser Configuration ====================
    browser: Literal["chrome", "firefox", "edge", "safari"] = Field(default="chrome", description="Browser to use")
    headless: bool = Field(default=False, description="Run browser in headless mode")
    window_size: str = Field(default="1920,1080", description="Browser window size")

    # ==================== Timeouts ====================
    implicit_wait: int = Field(default=10, ge=0, le=60, description="Implicit wait timeout in seconds")
    explicit_wait: int = Field(default=20, ge=0, le=120, description="Explicit wait timeout in seconds")
    page_load_timeout: int = Field(default=30, ge=0, le=120, description="Page load timeout in seconds")

    # ==================== Environment ====================
    environment: Literal["dev", "qa", "staging", "prod"] = Field(default="staging", description="Test environment")
    test_env: str = Field(default="qa", description="Test environment identifier")

    # ==================== Reporting ====================
    generate_allure_report: bool = Field(default=True, description="Generate Allure reports")
    screenshot_on_failure: bool = Field(default=True, description="Take screenshots on test failure")

    # ==================== Database (Optional) ====================
    db_host: Optional[str] = Field(default="localhost", description="Database host")
    db_port: Optional[int] = Field(default=5432, description="Database port")
    db_name: Optional[str] = Field(default="test_db", description="Database name")
    db_user: Optional[str] = Field(default="db_user", description="Database user")
    db_password: Optional[str] = Field(default="db_pass", description="Database password")

    # ==================== API Configuration ====================
    api_key: Optional[str] = Field(default=None, description="API key")
    api_secret: Optional[str] = Field(default=None, description="API secret")

    # ==================== Notifications ====================
    slack_webhook_url: Optional[str] = Field(default=None, description="Slack webhook URL")
    enable_notifications: bool = Field(default=False, description="Enable Slack/Teams notifications")

    # ==================== Remote Grid ====================
    use_remote_driver: bool = Field(default=False, description="Use remote WebDriver")
    remote_url: Optional[str] = Field(default="http://localhost:4444/wd/hub", description="Remote WebDriver URL")
    browserstack_username: Optional[str] = Field(default=None, description="BrowserStack username")
    browserstack_access_key: Optional[str] = Field(default=None, description="BrowserStack access key")

    # ==================== Paths ====================
    @property
    def base_dir(self) -> Path:
        """Get project base directory"""
        return Path(__file__).resolve().parent.parent

    @property
    def screenshots_dir(self) -> Path:
        """Get screenshots directory"""
        path = self.base_dir / "screenshots"
        path.mkdir(exist_ok=True)
        return path

    @property
    def reports_dir(self) -> Path:
        """Get reports directory"""
        path = self.base_dir / "reports"
        path.mkdir(exist_ok=True)
        return path

    @property
    def logs_dir(self) -> Path:
        """Get logs directory"""
        path = self.base_dir / "logs"
        path.mkdir(exist_ok=True)
        return path

    # ==================== Validators ====================
    @validator("window_size")
    def validate_window_size(cls, v):
        """Validate window size format"""
        if "," not in v:
            raise ValueError("Window size must be in format 'width,height'")
        width, height = v.split(",")
        if not (width.isdigit() and height.isdigit()):
            raise ValueError("Window size must contain numeric values")
        return v

    @validator("browser")
    def validate_browser(cls, v):
        """Validate browser choice"""
        valid_browsers = ["chrome", "firefox", "edge", "safari"]
        if v.lower() not in valid_browsers:
            raise ValueError(f"Browser must be one of {valid_browsers}")
        return v.lower()

    # ==================== Helper Methods ====================
    def get_window_size_tuple(self) -> tuple:
        """Get window size as tuple"""
        width, height = self.window_size.split(",")
        return (int(width), int(height))

    def get_db_connection_string(self) -> str:
        """Get database connection string"""
        if all([self.db_host, self.db_port, self.db_name, self.db_user, self.db_password]):
            return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        return ""

    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment == "prod"

    def print_settings(self):
        """Print current settings (excluding sensitive data)"""
        print("\n" + "="*60)
        print("TEST CONFIGURATION")
        print("="*60)
        print(f"Environment: {self.environment}")
        print(f"Base URL: {self.base_url}")
        print(f"Browser: {self.browser}")
        print(f"Headless: {self.headless}")
        print(f"Window Size: {self.window_size}")
        print(f"Username: {self.valid_username}")
        print(f"Implicit Wait: {self.implicit_wait}s")
        print(f"Explicit Wait: {self.explicit_wait}s")
        print(f"Screenshots: {self.screenshot_on_failure}")
        print(f"Allure Reports: {self.generate_allure_report}")
        print(f"Remote Driver: {self.use_remote_driver}")
        print("="*60 + "\n")


# Create global settings instance
settings = Settings()


# Example usage
if __name__ == "__main__":
    settings.print_settings()