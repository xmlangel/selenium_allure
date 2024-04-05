import requests
from requests.auth import HTTPBasicAuth

import config.config as config
import utilities.CustomLogger as log

jira_url = config.JIRA_URL
username = config.JIRA_USER_NAME
api_token = config.JIRA_API_TOKEN
assignee = config.JIRA_ISSUE_ASSIGNEE
project_key = config.JIRA_PROJECT_KEY
issue_type = config.JIRA_ISSUE_TYPE

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json;charset=utf-8"  # UTF-8 인코딩 추가
}


def send_request(method, url, **kwargs):
    """
    HTTP 요청을 보내고 응답을 반환 한다.
    :param method: HTTP 메소드 ('get', 'post', 'put' 등)
    :param url: 요청 URL
    :param kwargs: 추가 인수 (headers, data, json 등)
    :return: 응답 객체
    """
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()  # 4xx, 5xx 응답을 예외로 처리
        return response
    except requests.exceptions.HTTPError as e:
        log.custom_logger().error(f"HTTP 에러 발생: {e}")
    except requests.exceptions.ConnectionError:
        log.custom_logger().error("네트워크 연결 문제 발생")
    except requests.exceptions.Timeout:
        log.custom_logger().error("요청 시간 초과")
    except Exception as e:
        log.custom_logger().error(f"알 수 없는 오류 발생: {e}")
    return None


def create_issue(summary, project_key, issuetype, assignee_user_id=None):
    """
    지라 이슈를 생성한다.
    :param summary:  요약
    :param project_key: 프로젝트키
    :param issuetype: 이슈타입 (Bug, Task, Test 등을 지정)
    :param assignee_user_id: 담당자
    :return:
    """
    create_issue_endpoint = '/rest/api/3/issue/'

    # 이슈 생성을 위한 데이터, 이번에는 JIRA Wiki markup을 사용
    payload = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": "이 이슈는 자동화 테스트 실패로 발생한 이슈입니다. ",
                                "type": "text"
                            }
                        ]
                    },
                    {
                        "type": "orderedList",
                        "content": [
                            {
                                "type": "listItem",
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {
                                                "text": "테스트 스텝은 링크된 테스트를 참고 하시면됩니다 .",
                                                "type": "text"
                                            }
                                        ]
                                    }
                                ]
                            },
                            # 여기에 추가적인 리스트 아이템들을 넣을 수 있습니다.
                        ]
                    },
                ]
            },
            "issuetype": {
                "name": issuetype
            }
        }
    }
    # assignee가 있는 경우에만 추가
    if assignee_user_id:
        payload["fields"]["assignee"] = {"id": assignee_user_id}
    # 이슈 생성 요청
    response = send_request(
        'post',
        jira_url + create_issue_endpoint,
        headers=headers,
        auth=HTTPBasicAuth(username, api_token),
        json=payload
    )
    # 응답 확인
    if response.status_code == 201:
        issue_key = response.json()['key']
        log.custom_logger().info(f"이슈가 생성되었습니다: {jira_url}/browse/{issue_key}")
        return issue_key
    else:
        log.custom_logger().error("이슈 생성 실패:", response.content.decode('utf-8'))  # 오류 메시지 디코딩
        return None


# 파일 첨부를 위한 함수
def attach_file(issue_key, file_path):
    """
    지라 이슈에 파일을 첨부한다.
    :param issue_key: 이슈 번호
    :param file_path: 파일경로
    :return:
    """
    # 파일 첨부를 위한 엔드포인트
    attach_file_endpoint = f'/rest/api/3/issue/{issue_key}/attachments'

    # 파일 열기
    files = {
        "file": (file_path, open(file_path, 'rb'), 'application/octet-stream')
    }

    # 파일 첨부를 위한헤더 설정
    headers = {
        "X-Atlassian-Token": "no-check"
    }
    # 파일 첨부 요청
    response = send_request(
        'post',
        jira_url + attach_file_endpoint,
        headers=headers,
        files=files,
        auth=HTTPBasicAuth(username, api_token)
    )

    # 응답 확인
    if response.status_code == 200:
        pass
    else:
        log.custom_logger().error("파일 첨부 실패:", response.content)


# 이슈 링크를 생성하기 위한 함수
def link_issues(inward_issue_key, outward_issue_key, link_type):
    """
    이슈를 연결해준다.
    :param inward_issue_key:
    :param outward_issue_key:
    :param link_type:
    :return:
    """
    link_issues_endpoint = '/rest/api/3/issueLink'
    # 이슈 링크 생성을 위한 데이터
    payload = {
        "type": {
            "name": link_type
        },
        "inwardIssue": {
            "key": inward_issue_key
        },
        "outwardIssue": {
            "key": outward_issue_key
        }
    }
    # 이슈 링크 생성 요청
    response = send_request(
        'post',
        jira_url + link_issues_endpoint,
        headers=headers,
        auth=HTTPBasicAuth(username, api_token),
        json=payload
    )
    # 응답 확인
    if response.status_code == 201:
        log.custom_logger().info(
            f"이슈 링크가 성공적으로 생성되었습니다: {inward_issue_key} to {outward_issue_key}")
    else:
        log.custom_logger().error("이슈 링크 생성 실패:", response.content.decode('utf-8'))


# 사용자 ID를 얻어오는 함수
def get_account_id(user_email):
    """
    account_id 정보를 가져온다.
    :param user_email:
    :return:
    """
    # 사용자 검색을 위한 API 엔드포인트
    search_user_endpoint = f'/rest/api/3/user/search?query={user_email}'
    # 사용자 정보 요청
    response = send_request(
        'get',
        jira_url + search_user_endpoint,
        headers=headers,
        auth=HTTPBasicAuth(username, api_token)
    )
    # 응답 확인
    if response.status_code == 200:
        users = response.json()
        # 이메일 주소가 정확히 일치하는 첫 번째 사용자의 ID 반환
        for user in users:
            if user['emailAddress'].lower() == user_email.lower():
                return user['accountId']
        log.custom_logger().info("사용자를 찾을 수 없습니다.")
        return None
    else:
        log.custom_logger().error("사용자 정보 요청 실패:", response.content.decode('utf-8'))
        return None


def get_issue_link_types():
    """
    이슈 링크의 유형을 가져온다.
    :return:
    """
    link_types_endpoint = '/rest/api/3/issueLinkType'

    response = send_request(
        'get',
        jira_url + link_types_endpoint,
        headers=headers,
        auth=HTTPBasicAuth(username, api_token)
    )

    if response.status_code == 200:
        link_types = response.json()
        return link_types['issueLinkTypes']
    else:
        log.custom_logger().error("이슈 링크 유형 요청 실패:", response.content.decode('utf-8'))
        return None


# 이슈에 알림을 보내는 함수
def send_notification(issue_id_or_key, account_id):
    """
    Jira  알림을 발송한다.
    :param issue_id_or_key:
    :param account_id:
    :return:
    """
    notify_endpoint = f'/rest/api/3/issue/{issue_id_or_key}/notify'

    # 알림 내용 예시
    payload = {
        "subject": "자동화 테스트 이슈 할당 알림",
        "textBody": "할당된 이슈를 확인해주세요.",
        "htmlBody": "<p>이 티켓은 자동으로 할당된 이슈입니다. 할당된 이슈를 확인해주세요.</p>",
        "to": {
            "reporter": True,
            "assignee": True,
            "users": [
                {
                    "accountId": account_id  # 알림을 받을 사용자의 계정 ID
                }
            ]
        },
        "restrict": {
            "permissions": [
                {
                    "key": "BROWSE"
                }
            ]
        }
    }
    # 알림 요청
    response = send_request(
        'post',
        jira_url + notify_endpoint,
        headers=headers,
        auth=HTTPBasicAuth(username, api_token),
        json=payload
    )

    # 응답 확인
    if response.status_code == 204:
        log.custom_logger().info("알림이 성공적으로 전송되었습니다.")
    else:
        log.custom_logger().error(f"알림 전송 실패: {response.status_code} - {response.content.decode('utf-8')}")


# 이슈의 Summary를 가져오는 함수
def get_issue_summary(issue_id_or_key):
    """
    Jira Issue 의 summary 정보를 가져온다.
    :param issue_id_or_key:
    :return:
    """
    # 이슈 정보를 위한 API 엔드포인트
    issue_endpoint = f'/rest/api/3/issue/{issue_id_or_key}'

    # 이슈 요청
    response = send_request(
        'get',
        jira_url + issue_endpoint,
        headers=headers,
        auth=HTTPBasicAuth(username, api_token)
    )

    # 응답 확인
    if response.status_code == 200:
        issue_data = response.json()
        summary = issue_data['fields']['summary']
        return summary
    else:
        log.custom_logger().error(f"이슈 정보 요청 실패: {response.status_code} - {response.content.decode('utf-8')}")
        return None


def create_jira_issue(context):
    test_key = str(context.tags).strip("{}'")
    bug_tag = "[자동화 테스트] "
    bug_summary = get_issue_summary(test_key)
    account_id = get_account_id(assignee)
    if account_id:
        issue_key = create_issue(bug_tag + bug_summary, project_key, issue_type, account_id)
        if issue_key:
            link_issues(test_key, issue_key, 'Test')
            attach_file(issue_key, context.image_file_path)
            send_notification(issue_key, account_id)
        else:
            log.custom_logger().error("Jira Issue key 없음")
    else:
        log.custom_logger().error("Jira Issue 생성실패 (account_id 없음)")
