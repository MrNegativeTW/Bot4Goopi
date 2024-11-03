from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from gui.main_window import Application
# from bot.bot import Bot


def main():
    app = Application()  # Initialize the GUI
    app.mainloop()
    # bot = Bot()         # Initialize the bot
    # app.run(bot)

if __name__ == "__main__":
    main()
