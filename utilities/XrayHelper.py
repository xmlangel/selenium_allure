import requests
import json
import config.config as config

URL = "https://xray.cloud.getxray.app"


def post_execution(data):
    url = URL + "/api/v2/import/execution"
    response = requests.post(url, headers=set_headers(), data=data.encode('utf-8'))
    return response


def get_token():
    url = URL + "/api/v2/authenticate"

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "client_id": config.XRAY_CLIENT_ID,
        "client_secret": config.XRAY_CLIENT_SECRET
    }

    response = requests.post(url, headers=headers, json=data)
    return response.text


def set_headers():
    token = get_token()
    headers = {
        "Content-Type": "application/json",
        "charset": "utf-8",
        "Authorization": "Bearer " + token.replace('"', '')
    }
    return headers


def get_cucumber(keys):
    """
    xray token을 받아서 Jira 에등록된 cucumber 케이스를 받아온다.
    :param keys: SEN-690
    :return:
    """
    url = URL + "/api/v2/export/cucumber?keys=" + keys
    response = requests.get(url, headers=set_headers())
    return response


def create_test_report(info, tests):
    """
    info 와 tests json 을 생성해준다.
    :param info:
    :param tests:
    :return:
    """
    report = {
        "info": json.loads(info.replace('\n', '')),
        "tests": json.loads(tests.replace('\\', '')),
    }
    return json.dumps(report, indent=4, ensure_ascii=False)


def create_test_report_with_execute_key(execute_key, info, tests):
    """
    testExecutionKey, info, tests json을 생성해준다.
    :param execute_key:
    :param info:
    :param tests:
    :return:
    """
    report = {
        "testExecutionKey": execute_key,
        "info": json.loads(info.replace('\n', '')),
        "tests": json.loads(tests.replace('\\', '')),
    }
    return json.dumps(report, indent=4, ensure_ascii=False)


def info_append(info_data, summary, description, startDate, finishDate, testPlanKey, testEnvironments):
    """
    info json 값을 추가 해준다.
    :param info_data:
    :param summary:
    :param description:
    :param startDate:
    :param finishDate:
    :param testPlanKey:
    :param testEnvironments:
    :return:
    """
    info_data["summary"] = summary
    info_data["description"] = description
    info_data["startDate"] = startDate
    info_data["finishDate"] = finishDate
    info_data["testPlanKey"] = testPlanKey
    info_data["testEnvironments"] = testEnvironments
    return info_data


def tests_append(tests, testKey, start, finish, comment, status):
    """
    tests json 을 추가해준다.
    :param testKey:
    :param start:
    :param finish:
    :param comment:
    :param status:
    :return:
    """
    test = {
        "testKey": testKey,
        "start": start,
        "finish": finish,
        "comment": comment,
        "status": status,
    }
    tests.append(test)
    return tests


def tests_append_to_file(testKey, start, finish, comment, status):
    """
    result.json 을 추가해준다.
    :param testKey:
    :param start:
    :param finish:
    :param comment:
    :param status:
    :return:
    """
    test = {
        "testKey": testKey,
        "start": start,
        "finish": finish,
        "comment": comment,
        "status": status,
    }

    try:
        with open("result.json", "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []
    
    matching_tests = [t for t in existing_data if t["testKey"] == testKey]

    if status == "FAILED":
        for existing_test in matching_tests:
            existing_test["status"] = "FAILED"
            existing_test["comment"] = "FAILED"

    existing_data.append(test)
    with open("result.json", "w") as json_file:
        json.dump(existing_data, json_file, indent=4, ensure_ascii=False)


def write_result(start, end):
    """
    xray 에 테스트 결과 기록
    :return:
    """
    info_data = dict()
    summary = "Firescout 2.0 UI 자동화 테스트 수행"
    description = "Firescout 2.0 UI 자동화 테스트 수행을 위한 고정 티켓입니다.\n이 실행결과는 외부 소스에서 실행 결과를 가져와 자동으로 테스트 결과를 기록한 파일입니다."
    testEnvironments = ["web"]

    with open("result.json", "r") as json_file:
        existing_data = json.load(json_file)
        
    tests = existing_data
    info_data = info_append(info_data, summary, description, start, end,
                            config.XRAY_TEST_PLAN_KEY,
                            testEnvironments)

    info = json_make(info_data)
    tests = json_make(tests)

    result = create_test_report_with_execute_key(config.XRAY_TEST_EXECUTION_KEY, info, tests)

    if (config.XRAY_SAVE_RESULT):
        response = post_execution(result)
        print(response.text)
        return response.text
    else:
        print("==xray not save==")
        print(result)


def json_make(data):
    return json.dumps(data, ensure_ascii=False)
