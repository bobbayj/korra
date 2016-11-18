FROM danielquinn/django

# Install build dependencies
RUN apk update && \
  apk add gcc musl-dev libffi-dev

# Python dependencies
COPY /requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Cleanup
RUN apk del gcc && \
  rm /var/cache/apk/*

# Copy the local directory into the app directory
COPY / /app

