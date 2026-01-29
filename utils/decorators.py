"""
Decorators for logging and monitoring test execution.
"""

import logging
import functools
import time
from typing import Any, Callable

logger = logging.getLogger(__name__)


def log_method(func: Callable) -> Callable:
    """
    Decorator to log method calls, arguments, return values, and execution time.

    Usage:
        @log_method
        def my_method(self, arg1, arg2):
            return "result"
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get class name and method name
        class_name = args[0].__class__.__name__ if args else "Unknown"
        method_name = func.__name__

        # Log method entry
        logger.info(f"{'=' * 60}")
        logger.info(f"🔵 ENTERING: {class_name}.{method_name}()")

        # Log arguments (skip 'self')
        if len(args) > 1:
            logger.info(f"   📥 Args: {args[1:]}")
        if kwargs:
            logger.info(f"   📥 Kwargs: {kwargs}")

        # Execute method and measure time
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time

            # Log success
            logger.info(f"   ✅ SUCCESS")
            if result is not None:
                logger.info(f"   📤 Return: {result}")
            logger.info(f"   ⏱️  Time: {execution_time:.3f}s")
            logger.info(f"{'=' * 60}\n")

            return result

        except Exception as e:
            execution_time = time.time() - start_time

            # Log failure
            logger.error(f"   ❌ FAILED: {class_name}.{method_name}()")
            logger.error(f"   💥 Error: {type(e).__name__}: {str(e)}")
            logger.error(f"   ⏱️  Time: {execution_time:.3f}s")
            logger.error(f"{'=' * 60}\n")

            raise

    return wrapper


def log_page_state(func: Callable) -> Callable:
    """
    Decorator to log page state before and after method execution.

    Usage:
        @log_page_state
        def navigate_to(self, url):
            self.driver.get(url)
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, 'driver'):
            try:
                current_url = self.driver.current_url
                title = self.driver.title
                logger.info(f"📍 Before: URL={current_url}, Title={title}")
            except Exception as e:
                logger.warning(f"📍 Before: Could not get page state - {e}")

        result = func(self, *args, **kwargs)

        if hasattr(self, 'driver'):
            try:
                current_url = self.driver.current_url
                title = self.driver.title
                logger.info(f"📍 After: URL={current_url}, Title={title}")
            except Exception as e:
                logger.warning(f"📍 After: Could not get page state - {e}")

        return result

    return wrapper