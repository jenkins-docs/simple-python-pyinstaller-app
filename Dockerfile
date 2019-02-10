FROM alpine
FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# include pylint and pytest
RUN pip install docker-py feedparser nosexcover prometheus_client pycobertura pylint pytest pytest-cov requests setuptools sphinx
RUN wget -qO /usr/local/bin/qcoverage  https://github.com/qnib/qcoverage/releases/download/v0.1/qcoverage_v0.1_Linux \
 && chmod +x /usr/local/bin/qcoverage
 
ARG PYINSTALLER_VERSION=3.1.1
ARG PYSCHEMA_VERSION=0.6.5
ARG PYYAML_VERSION=3.12
RUN $PYTHON -m pip install pyinstaller==$PYINSTALLER_VERSION pyyaml==$PYYAML_VERSION schema==$PYSCHEMA_VERSION
 
#include pyinstaller
# RUN pip install pyinstaller && \
    useradd -m -s /bin/bash pyinstaller
# Set the user to use when running a container
#USER pyinstaller

# Container will by default run 'pyinstaller --help'
# ENTRYPOINT [ "pyinstaller" ]
# CMD [ "--help" ]

CMD ["gunicorn", "-w 4", "main:app"]
