import argparse
import timeit


def run_behave_with_timeit(feature_file, repetition):
    setup_code = '''
from behave.__main__ import main as behave_main
    '''

    test_code = f'''
for _ in range({repetition}):
    behave_main(["{feature_file}"])
    '''

    # timeit를 사용하여 특정 기능 파일을 repetition 횟수만큼 반복 실행한 후 실행 시간 측정
    execution_time = timeit.timeit(stmt=test_code, setup=setup_code, number=1)
    print(f"{feature_file}을(를) {repetition}번 반복 실행한 결과 - 실행 시간: {execution_time:.2f} 초")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Behave 테스트 반복 실행 및 시간 측정")
    # feature_file 매개변수 설명 추가
    parser.add_argument("feature_file", help="실행할 Behave 특정 기능 파일의 경로")
    # repetition 매개변수 설명 추가
    parser.add_argument("repetition", type=int, help="테스트를 반복할 횟수")
    args = parser.parse_args()
    run_behave_with_timeit(args.feature_file, args.repetition)
