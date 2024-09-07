import os
import uuid
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright


def capture_screenshot(url: str) -> str:
    """
    Captures a screenshot of the given URL and saves it to a file.

    Args:
        url (str): The URL of the webpage to capture.

    Returns:
        str: The file path of the saved screenshot.
    
    Raises:
        ValueError: If the URL is invalid or not accessible.
        OSError: If an error occurs while saving the screenshot.
    """
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.hostname:
            raise ValueError("Invalid URL provided")

        website_host_name = parsed_url.hostname
        screenshot_id = str(uuid.uuid4())

        # Create directory to store screenshots
        directory_path = os.path.join("cache", website_host_name)
        os.makedirs(directory_path, exist_ok=True)

        # Define screenshot file path
        screenshot_path = os.path.join(directory_path, f"{screenshot_id}.png")

        # Use Playwright to capture the screenshot
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            page.screenshot(path=screenshot_path, full_page=True)
            browser.close()

        print(f"Screenshot saved at {screenshot_path}")
        return screenshot_path

    except Exception as e:
        raise OSError(f"Failed to capture screenshot: {e}")
