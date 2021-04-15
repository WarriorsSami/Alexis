from selenium import webdriver

DRIVER_PATH = r"./drivers/"


class WebDriverCreator:

    @staticmethod
    def create(browser):
        browser = browser.lower()

        if "chrome" in browser:
            return webdriver.Chrome(DRIVER_PATH + browser)
        if "edge" in browser:
            return webdriver.Edge(DRIVER_PATH + browser)
        if "firefox" in browser:
            return webdriver.Firefox(DRIVER_PATH + browser)
        if "safari" in browser:
            return webdriver.Safari(DRIVER_PATH + browser)
        if "opera" in browser:
            return webdriver.Opera(DRIVER_PATH + browser)
