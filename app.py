from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from utils import random_shit as RandomShits
from gui.main_window import Application

def main():
    RandomShits.print_welcome_box()
    app = Application()  # Initialize the GUI
    app.mainloop()
    # bot = Bot()         # Initialize the bot
    # app.run(bot)

if __name__ == "__main__":
    main()
