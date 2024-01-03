#!/bin/bash

rm -rf reports/allure-report
allure generate reports/allureReports -o reports/allure-report
allure-combine ./reports/allure-report --dest ./reports
open ./reports/complete.html
