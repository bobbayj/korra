FROM python:3.5-alpine

# Install build dependencies
RUN apk update
RUN apk add gcc musl-dev libffi-dev postgresql-dev

# Install the dependencies before copying the source code as this prevents
# frequent docker  build commands from having to keep re-installing the same
# dependencies over and over
COPY /requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the local directory into the app directory
COPY / /app
