from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from config import PATH_TO_WEBDRIVER, SCREENSHOT_WIDTH, logger
from exceptions import SeleniumException


def open_web_site(url: str) -> WebDriver:
    """
    Open web site using selenium with chrome webdriver.
    Works in headless mode with disabled javascript and other static.
    :param url: str, received url
    :return: WebDrivers instance
    """
    try:
        chrome_options = Options()

        # Disable all JavaScript and static elements
        prefs = {
            "profile.default_content_setting_values": {
                "cookies": 2,
                "images": 2,
                "javascript": 2,
                "plugins": 2,
                "popups": 2,
                "geolocation": 2,
                "notifications": 2,
                "auto_select_certificate": 2,
                "fullscreen": 2,
                "mouselock": 2,
                "mixed_script": 2,
                "media_stream": 2,
                "media_stream_mic": 2,
                "media_stream_camera": 2,
                "protocol_handlers": 2,
                "ppapi_broker": 2,
                "automatic_downloads": 2,
                "midi_sysex": 2,
                "push_messaging": 2,
                "ssl_cert_decisions": 2,
                "metro_switch_to_desktop": 2,
                "protected_media_identifier": 2,
                "app_banner": 2,
                "site_engagement": 2,
                "durable_storage": 2,
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-javascript")

        # Headless mode
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("start-maximized")

        # Open web-page
        driver: webdriver.Chrome = webdriver.Chrome(
            executable_path=PATH_TO_WEBDRIVER, chrome_options=chrome_options
        )
        driver.get(url)

        # Set size of window for making screenshot
        required_height: int = driver.execute_script(
            "return document.body.parentNode.scrollHeight"
        )
        driver.set_window_size(SCREENSHOT_WIDTH, required_height)
        return driver
    except Exception:
        logger.error("Failed on the selenium open page: ", exc_info=True)
        raise SeleniumException("Error. Check your url or try later.")
