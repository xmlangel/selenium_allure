docker run -d --rm  \
--name selenium-grid  \
-p 4444:4444  \
-p 7900:7900 \
--shm-size="2g" \
selenium/standalone-chrome:latest