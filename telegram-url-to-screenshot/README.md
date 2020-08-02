# Main requirements:
- Python 3.8
- python-telegram-bot 12.8
- ChromeDriver 84.0
- Selenium 3.141
- poetry

# Description 
The bot responds to receiving messages from the user containing a link to a web page.

Then, using selenium and chrome webdriver with *disabled JavaScript, other statics and extensions*, the page is loaded and a screenshot is created in *1920xfull_height* format.

The image is saved in the directory and sent to the user. If the image size exceeds the allowed limit, it is sent as a file.

The image is removed from the directory.

*Logging of errors* was provided and exceptions were created.

# Run
To start the bot, you need to set the bot token `BOT_TOKEN` in the environment variable and run `python main.py`.

# Note
To improve the style of the code were applied: isort, black, pylint
(contact the developer for their configs).

# License
**Skype**: dinamo.mutu
