from WebDriverCreator import WebDriverCreator
from util import getAppConfig
from app import App
import time

config = getAppConfig()

App = App(config)
App.run()
