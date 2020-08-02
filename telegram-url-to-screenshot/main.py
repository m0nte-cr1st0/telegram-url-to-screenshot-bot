import os

from selenium.webdriver.chrome.webdriver import WebDriver
from telegram import Bot, Update
from telegram.error import BadRequest
from telegram.ext import (
    CallbackContext,
    Dispatcher,
    Filters,
    MessageHandler,
    Updater,
)

from config import BOT_TOKEN, SCREENSHOT_DIR, SCREENSHOT_NAME, logger
from exceptions import SeleniumException, TelegramException
from parsing import open_web_site


# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
bot: Bot = Bot(token=BOT_TOKEN)
updater: Updater = Updater(bot=bot, use_context=True)


def make_screenshot(driver: WebDriver) -> None:
    """
    Creates screenshot of opened page.
    :param driver: WebDrivers instance
    :return: None
    """
    try:
        driver.save_screenshot(SCREENSHOT_DIR + SCREENSHOT_NAME)
    except Exception:
        logger.error("Failed on the selenium save image: ", exc_info=True)
        raise SeleniumException("Error. Try later.")


def send_image(update: Update) -> None:
    """
    Sends screenshot to telegram chat.
    :param update: Update instance
    :return: None
    """
    try:
        try:
            bot.send_photo(
                update.message.chat_id,
                photo=open(SCREENSHOT_DIR + SCREENSHOT_NAME, "rb"),
            )
        except BadRequest:
            bot.send_document(
                update.message.chat_id,
                document=open(SCREENSHOT_DIR + SCREENSHOT_NAME, "rb"),
            )
    except Exception:
        logger.error("Failed on the telegram send image: ", exc_info=True)
        raise TelegramException("Error. Try later.")


def send_error_message(update: Update, message: str) -> None:
    """
    Send message about error to telegram chat.
    :param update: Update instance
    :param message: Error message text
    :return: None
    """
    try:
        bot.send_message(update.message.chat_id, text=message)
    except Exception:
        pass


def remove_image() -> None:
    """Removes image from directory if it exists"""
    try:
        os.remove(SCREENSHOT_DIR + SCREENSHOT_NAME)
    except OSError:
        pass


def get_images(update: Update, context: CallbackContext) -> None:
    """
    Main function. Runs other functions.
    :param update: Update instance
    :param context: CallbackContext
    :return: None
    """
    url: str = update.message.text
    try:
        driver: WebDriver = open_web_site(url)
        make_screenshot(driver)
        driver.close()
    except SeleniumException as error:
        return send_error_message(update, str(error))
    else:
        driver.quit()
    try:
        send_image(update)
    except TelegramException as error:
        send_error_message(update, str(error))
    return remove_image()


def main() -> None:
    """Start the bot."""
    # Get the dispatcher to register handlers
    dispatcher: Dispatcher = updater.dispatcher

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, get_images)
    )

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
