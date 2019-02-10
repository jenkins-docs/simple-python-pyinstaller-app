FROM alpine
FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install docker-py feedparser nosexcover prometheus_client pycobertura pylint pytest pytest-cov requests setuptools sphinx
RUN wget -qO /usr/local/bin/qcoverage  https://github.com/qnib/qcoverage/releases/download/v0.1/qcoverage_v0.1_Linux \
 && chmod +x /usr/local/bin/qcoverage
CMD ["gunicorn", "-w 4", "main:app"]
