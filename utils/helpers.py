"""
Utility helper functions
"""
import random
import string
from datetime import datetime
from faker import Faker
from utils.logger import logger

fake = Faker()


class TestDataGenerator:
    """Generate test data"""

    @staticmethod
    def generate_random_email() -> str:
        """Generate random email"""
        return fake.email()

    @staticmethod
    def generate_random_username() -> str:
        """Generate random username"""
        return fake.user_name()

    @staticmethod
    def generate_random_password(length: int = 12) -> str:
        """Generate random strong password"""
        characters = string.ascii_letters + string.digits + "!@#$%^&*()"
        return ''.join(random.choices(characters, k=length))

    @staticmethod
    def generate_random_phone() -> str:
        """Generate random phone number"""
        return fake.phone_number()

    @staticmethod
    def generate_random_address() -> dict:
        """Generate random address"""
        return {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip": fake.zipcode(),
            "country": fake.country()
        }


class DateTimeHelper:
    """DateTime utility functions"""

    @staticmethod
    def get_timestamp(format: str = "%Y%m%d_%H%M%S") -> str:
        """Get formatted timestamp"""
        return datetime.now().strftime(format)

    @staticmethod
    def get_date(format: str = "%Y-%m-%d") -> str:
        """Get formatted date"""
        return datetime.now().strftime(format)


class StringHelper:
    """String manipulation utilities"""

    @staticmethod
    def truncate(text: str, length: int = 50) -> str:
        """Truncate string to specified length"""
        return text[:length] + "..." if len(text) > length else text

    @staticmethod
    def clean_filename(filename: str) -> str:
        """Clean filename for safe file system use"""
        return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()