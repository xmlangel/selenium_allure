## 필요 패키지 설치
 - selenium
 - behave
 - allure-behave
### pip install -r requirements.txt

## behave 를 통해서 allure report 생성 및 실행(예시파일은 login.feture를 실행하는 스크립트)
```shell
behave -f allure_behave.formatter:AllureFormatter -o reports features/login.feature
```
 
## allure report 보기
```shell
allure serve reports
```

### 기타 자세한 사항은 아래 링크참고
https://docs.qameta.io/allure/#_reporting

실행예시
```shell
python3 -m venv venv
source venv/bin/activate
behave -f allure_behave.formatter:AllureFormatter -o reports features/login.feature 
```
