FROM python:3.9-slim-buster

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv

RUN apt-get update && apt-get install -y libaio1 wget unzip tzdata && apt-get install -y git
# timezone to +0
ENV TZ=Asia/Almaty
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./instantclient_19_21 /opt/oracle/instantclient19

WORKDIR /opt/oracle
# RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip && \
#     unzip instantclient-basiclite-linuxx64.zip && rm -f instantclient-basiclite-linuxx64.zip && \
#     cd /opt/oracle/instantclient* && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci && \
#     echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && ldconfig
RUN ln -s /opt/oracle/instantclient19/libclntsh.so.19.1 /usr/lib/libclntsh.so.19.1
RUN ln -s /opt/oracle/instantclient19/libnnz19.so /usr/lib/libnnz19.so
RUN ln -s /opt/oracle/instantclient19/libclntshcore.so.19.1 /usr/lib/libclntshcore.so.19.1

RUN echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && ldconfig

WORKDIR /app

# Install wget
RUN apt-get update && apt-get install libssl-dev wkhtmltopdf -y

# Copy Pipfile and Pipfile.lock
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy project
COPY . .