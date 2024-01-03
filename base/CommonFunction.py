import config.config
from base.BasePage import BasePage
from selenium import webdriver
import utilities.CustomLogger as cl

class CommonFunction(BasePage):

    def __init__(self, driver, context):
        self.driver = driver
        self.context = context

    def open_new_window(self):
        BasePage.excute_script_window_open(self)
        cl.allure_logs("open_new_window")

    def switch_to_window(self, switch_number):
        BasePage.switch_to_window(self, switch_number)
        cl.allure_logs("switch to windows")

    def refresh_page(self):
        BasePage.refresh_page(self)
        cl.allure_logs("refresh")
