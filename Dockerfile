FROM python:3.7-alpine

# Ensures that the python output is sent straight to terminal
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# --no-cache: after update of the registry,
# don't store the registry index in the docker container
# it's a best practice to keep the docker container to have the smallest
# footprint possible, the lean container
RUN apk add --update --no-cache postgresql-client

# --virtual: sets an alias for dependencies that could be used to easily
# remove unnecessary dependencies later
RUN apk add --update --no-cache --virtual .temp-build-deps \
      gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

RUN apk del .temp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# System user to run the processes
# To avoid running our app with the root user
RUN adduser -D user
USER user
