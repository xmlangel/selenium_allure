import string
import random
import json
import datetime
import os


def make_random_string(length):
    """
    length 만큼 random 값을 만들어준다.
    :param length:
    :return:
    """
    string_pool = string.ascii_lowercase  # 소문자
    randomstr = []  # 결과 값
    for i in range(length):
        result = random.choice(string_pool)  # 랜덤한 문자열 하나 선택
        randomstr.append(result)
    resultstr = ''.join(randomstr)
    return resultstr


def join_number(numlist):
    """
    numlist 로 들어온값과 random으로 8자리 숫자를 문들어준다.
    :param numlist:
    :return:
    """
    for i in range(8):  # 8자리 숫자 리스트 생성
        num = random.randrange(0, 9)
        numlist.append(num)
    resultlist = ''.join(map(str, numlist))
    return resultlist


def make_random_string(length):
    # _LENGTH = 10  # 10자리
    string_pool = string.ascii_lowercase  # 소문자
    randomstr = []  # 결과 값
    for i in range(length):
        result = random.choice(string_pool)  # 랜덤한 문자열 하나 선택
        randomstr.append(result)
    resultstr = ''.join(randomstr)
    return resultstr


def json_make(data):
    return json.dumps(data, ensure_ascii=False)


def get_formatted_date_time(timestamp):
    """
    unixTime 시간을
    "%Y-%m-%dT%H:%M:%S"+"+09:00" 형식으로 출력
    :param timestamp:
    :return:
    """
    dt = datetime.datetime.fromtimestamp(timestamp)
    # 날짜 형식으로 날짜와 시간 출력
    formatted_date_time = dt.strftime("%Y-%m-%dT%H:%M:%S" + "+09:00")
    return formatted_date_time


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f'{file_path} 파일이 삭제되었습니다.')
    except FileNotFoundError:
        print(f'{file_path} 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'파일 삭제 중 오류가 발생했습니다: {e}')
