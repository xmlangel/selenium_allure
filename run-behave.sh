#!/bin/sh
LOCAL_PATH=$(pwd)
rm -rf $LOCAL_PATH/reports/allureReports
behave  -f  allure_behave.formatter:AllureFormatter -o $LOCAL_PATH/reports/allureReports $1
# sh ./view-allure-report.sh
sh ./make-report.sh
sh ./delete-report.sh