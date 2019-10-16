from config import *
from selenium import webdriver
from bot import Bot

# Opens firefox browser, installs uBlock Origin extensions
driver = webdriver.Firefox()
driver.install_addon(AD_BLOCK_EXTENSION)

# Opens game website
driver.get(WEB_URL)

# Starts game
bot = Bot(driver)
started = bot.start_game()

# If game started successfully, scans text and then types that text to input box
if started:
    text = bot.scan_text()
    print(text)
    if text is not None:
        bot.enter_text(text)
