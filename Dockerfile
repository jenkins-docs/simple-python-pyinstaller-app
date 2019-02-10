FROM alpine
FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# include pylint and pytest
RUN pip install docker-py feedparser nosexcover prometheus_client pycobertura pylint pytest pytest-cov requests setuptools sphinx
RUN wget -qO /usr/local/bin/qcoverage  https://github.com/qnib/qcoverage/releases/download/v0.1/qcoverage_v0.1_Linux \
 && chmod +x /usr/local/bin/qcoverage
 
#include pyinstaller
RUN pip install pyinstaller && \
    useradd -m -s /bin/bash pyinstaller
# Set the user to use when running a container
USER pyinstaller

CMD ["gunicorn", "-w 4", "main:app"]
