import time

import config.config
import utilities.Helper as helper

start_time = None
end_time = None


def before_feature(context, feature):
    helper.delete_file('result.json')


def before_scenario(context, scenario):
    global start_time
    start_time = helper.get_formatted_date_time(time.time())


def after_scenario(context, scenario):
    global end_time
    end_time = helper.get_formatted_date_time(time.time())
    result = set_test_result(scenario)
    if (config.config.REMOTE_RUN):
        context.driver.quit()
    else:
        context.driver.close()


def set_test_result(scenario):
    """
    테스트 결과
    :param scenario:
    :return:
    """
    if "failed" in str(scenario.status):
        print("테스트 실패" + str(scenario.status))
        result = "FAILED"
    else:
        print("테스트 성공")
        result = "PASSED"
    return result


def after_feature(context, feature):
    pass
