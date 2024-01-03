import os

import allure
from allure_commons.types import AttachmentType
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import utilities.CustomLogger as log
import config.config as config
import time
from traceback import print_stack

waitTime = config.SELENIUM_WAIT_TIME
BASE_DIR = os.getcwd()
logger = log.custom_logger()


class BasePage:

    def __init__(self,driver,context):
        self.driver = driver
        self.context = context
    def actionChains(self):
        return ActionChains(self.driver)

    def take_screenshotoallure(self, text):
        allure.attach(self.driver.get_screenshot_as_png(), name=text, attachment_type=AttachmentType.PNG)

    def find_element(self, by_selector, locator):
        self.driver.implicitly_wait(waitTime)
        try:
            element = self.driver.find_element(by=by_selector, value=locator)
            self.highlight(element, 0, "red", 3)
            logger.info(f"Found element with locator: {locator}")
            return element
        except NoSuchElementException:
            self.write_log(locator, "Element Not Found")
            assert False

    def is_displayed(self, by_selector, locator):
        self.driver.implicitly_wait(waitTime)
        try:
            element = self.driver.find_element(by=by_selector, value=locator)
            element.is_displayed()
            self.highlight(element, 0, "red", 3)
            logger.info("Displayed locator value " + locator)
            return True
        except NoSuchElementException:
            self.write_log(locator, "No Displayed locator value ")
            assert False
            return False

    def click_element(self, by_selector, locator):
        self.driver.implicitly_wait(waitTime)
        try:
            element = self.driver.find_element(by=by_selector, value=locator)
            self.highlight(element, 0.1, "red", 3)
            element.click()

        except NoSuchElementException:
            self.write_log(locator, "Unable to Click with locator value ")
            assert False


    def write_log(self, locator, text):
        """
        로그와 스크린샷을 기록해준다.
        :param locator:
        :param text: 기록할 메세지
        :return:
        """
        print_stack()
        logger.info(text + locator)
        self.take_screenshotoallure(locator)
        self.save_screen_shot_tofile()

    def switch_to_window(self, handle_number):
        """
        handle_number 로 스위치 한다.
        :param handle_number:
        :return:
        """
        self.driver.switch_to.window(self.driver.window_handles[handle_number])