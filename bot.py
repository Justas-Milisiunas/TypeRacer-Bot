import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from config import *


class Bot:
    def __init__(self, driver):
        self.driver = driver

    # Scans text
    def scan_text(self):
        # Tries to find text box element
        try:
            items = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, TEXT))
            )

            for item in items:
                print(item.text)

            result = ""
            if len(items) is 2:
                result += items[0].text + items[1].text
            elif len(items) is 3:
                result += items[0].text + items[1].text + " " + items[2].text

            return result
        except NoSuchElementException as e:
            print(f"No text found: {e.msg}")
            return None
        except IndexError:
            print(f"Likely text structure changed")
            return None
        except TimeoutException as e:
            print(f"Text scan timeout: {e.msg}")
            return None

    # Enters given text to input box
    def enter_text(self, text):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, START_POPUP))
            )

            input_space = self.driver.find_element_by_xpath(INPUT_TEXT)
            for item in text:
                for letter in item:
                    time.sleep(TYPING_SPEED)
                    input_space.send_keys(letter)
        except NoSuchElementException as e:
            print(f"Input text box not found: {e.msg}")
        except TimeoutException as e:
            print(f"Timeout exception, game not started: {e.msg}")

    # Waits till main page is loaded and then starts game
    def start_game(self):
        try:
            start_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, GAME_START_BUTTON))
            )

            start_button.click()
            appeared = self.quest_popup_appreared()

            if not appeared:
                return True
            else:
                return False
        except NoSuchElementException:
            print("Enter a typing race button not found")
            return False
        except TimeoutException:
            print("Start game timeout exception")
            return False

    # Handles sometimes appearing popup
    def quest_popup_appreared(self):
        try:
            item = WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.XPATH, SELECT_QUEST_BUTTON))
            )

            item.click()
        except NoSuchElementException as e:
            print(f"Select to play as quest pop up not found {e.msg}")
            return False
        except TimeoutException as e:
            print(f"Select to play as guest timeout exception {e.msg}")
            return False
        else:
            return True
