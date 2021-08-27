FROM python:3.7-alpine

# Ensures that the python output is sent straight to terminal
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# System user to run the processes
# To avoid running our app with the root user
RUN adduser -D user
USER user
