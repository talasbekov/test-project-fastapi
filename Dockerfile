FROM python:3.9-slim-buster

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv

RUN apt-get update && apt-get install -y libaio1 wget unzip && apt-get install -y git

WORKDIR /opt/oracle
RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip && \
    unzip instantclient-basiclite-linuxx64.zip && rm -f instantclient-basiclite-linuxx64.zip && \
    cd /opt/oracle/instantclient* && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci && \
    echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && ldconfig

WORKDIR /app

# Install wget
RUN apt-get update && apt-get install libssl-dev wkhtmltopdf -y

# Copy Pipfile and Pipfile.lock
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy project
COPY . .
