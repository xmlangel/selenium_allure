from behave import *
import base64

from base.BasePage import BasePage
from base.CommonFunction import CommonFunction
from pages.MainPage import MainPage
import config.config as config

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import sys


@when
@given('크롬브라우저로 Google URL 에 접속한다.')
def step_impl(context):
    try:
        if not hasattr(context, 'driver'):
            if (config.REMOTE_RUN):
                remote_url_chrome(context)
            else:
                local_chrome(context)

        context.driver.get(config.URL)
        context.driver.implicitly_wait(3)
    except AttributeError as e:
        # 오류 메시지를 로그로 남기고 프로그램을 종료합니다.
        print(f"오류 발생: {e}")
        sys.exit(1)  # 프로그램 종료


def local_chrome(context):
    option = Options()
    option.add_argument("--lang=ko")  # 브라우저 언어 한국어로 지정
    service = Service()
    context.driver = webdriver.Chrome(service=service, options=option)


def remote_url_chrome(context):
    chrome_options = Options()
    chrome_options.add_argument("--lang=ko")  # 브라우저 언어 한국어로 지정
    chrome_options.set_capability("browserName", "chrome")
    try:
        context.driver = webdriver.Remote(
            command_executor=config.SELENIUM_GRID_URL,
            options=chrome_options
        )
    except Exception as e:
        # 오류 메시지를 로그로 남기고 프로그램을 종료합니다.
        print(f"오류 발생: {e}")
        sys.exit(1)  # 프로그램 종료
