"""
Enhanced Logging Configuration with Color Support
"""
import logging
import colorlog
from pathlib import Path
from datetime import datetime
from config.settings import settings


class Logger:
    """Custom logger with color support"""

    @staticmethod
    def get_logger(name: str = __name__) -> logging.Logger:
        """
        Get configured logger instance

        Args:
            name: Logger name

        Returns:
            logging.Logger: Configured logger
        """
        # Create logger
        logger = colorlog.getLogger(name)

        # Return if already configured
        if logger.handlers:
            return logger

        logger.setLevel(logging.DEBUG)

        # Console handler with colors
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(logging.INFO)

        console_format = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_format)

        # File handler (plain text)
        log_file = settings.logs_dir / f"test_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)

        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger


# Create default logger
logger = Logger.get_logger(__name__)