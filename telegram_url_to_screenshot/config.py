import logging
import os


logging.basicConfig(
    filename="errors.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.ERROR,
)
logger = logging.getLogger(__name__)


BOT_TOKEN = os.getenv("BOT_TOKEN")
PATH_TO_WEBDRIVER = "chromedriver.exe"
SCREENSHOT_DIR = "./screenshots/"
SCREENSHOT_NAME = "screenshot.png"
SCREENSHOT_WIDTH = 1920
