#!/bin/sh
LOCAL_PATH=$(pwd)
directory="$LOCAL_PATH/reports/"
# 7일이상 지난파일 삭제
find "$directory" -type f -mtime +7 -exec rm {} \;
allure serve -h 127.0.0.1 $LOCAL_PATH/reports/allureReports