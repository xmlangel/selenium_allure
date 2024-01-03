from base.BasePage import BasePage
from selenium.webdriver.common.by import By
import utilities.CustomLogger as cl
import time


class MainPage(BasePage):

  
    # 메인 페이지 영역
    def __init__(self, driver, context):
        super().__init__(driver, context)
        self.driver = driver
        self.context = context

    def show_logo(self):
        BasePage.is_displayed(self, By.XPATH, "/div/img")
        cl.allure_logs("로고 표시")

