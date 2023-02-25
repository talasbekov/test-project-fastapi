FROM python:3.9-slim-buster

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv

# Set working directory
WORKDIR /app

# Install wget
RUN apt-get update && apt-get install -y wget

# Copy Pipfile and Pipfile.lock
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy project
COPY . .
