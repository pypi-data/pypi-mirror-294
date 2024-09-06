import time
import requests
from io import BytesIO
from PIL import Image
from base64 import b64decode, b64encode

from appium.webdriver.webdriver import WebDriver

from .types import AppiumSessionConfig


def delay(milliseconds: int) -> None:
    """
    Delays execution for a given number of milliseconds.

    Args:
        milliseconds (int): Number of milliseconds to delay execution.
    """
    time.sleep(milliseconds / 1000)


def get_screenshot(driver: WebDriver) -> str:
    """
    Fetches a screenshot from the WebDriver session.

    Args:
        driver (WebDriver): The WebDriver instance.

    Returns:
        str: Base64 encoded screenshot.
    """
    screenshot = driver.get_screenshot_as_base64()

    # TODO add resizing of the image

    return screenshot
