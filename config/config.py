#
URL="https://google.co.kr"
#Report
PASS_SCREENSHOT=True # True: Pass 일경우에도 스크린샷 Allure리포트에 ScreenShoot 저장


#Selenium_Grid
REMOTE_RUN=False #True : selenium grid URL이용
SELENIUM_GRID_URL="[REMOTE_URL]" # temporary "http://192.168.1.100:4444/wd/hub"
SELENIUM_WAIT_TIME="[SELENIUM_WAIT_TIME]" 

#Xray
XRAY_SAVE_RESULT=False # True: Xray 에 테스트 결과 저장
XRAY_CLIENT_ID=""
XRAY_CLIENT_SECRET=""
XRAY_TEST_EXECUTION_KEY = ""
XRAY_TEST_PLAN_KEY = ""
#Selenium_Grid
REMOTE_RUN=False #True : selenium grid URL이용
SELENIUM_GRID_URL="http://127.0.0.1:33097/wd/hub" # temporary "http://192.168.1.100:4444/wd/hub"
SELENIUM_WAIT_TIME="10" # jenkins 가 좀 느려서 20이 적당한 것 같음

#JIRA
JIRA_ISSUE_CREATE=False #True : 테스트 fail 시 Jira Bug 티켓 생성
JIRA_USER_NAME=""
JIRA_API_TOKEN=""
JIRA_URL=""
JIRA_PROJECT_KEY=""
JIRA_ISSUE_ASSIGNEE=""
JIRA_ISSUE_TYPE=""
