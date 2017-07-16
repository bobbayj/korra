FROM danielquinn/django:debian

COPY /requirements.txt /app/requirements.txt

# Install build dependencies
RUN apt update &&
  apt install gcc libffi-dev && \
  pip install -r /app/requirements.txt && \
  apt remove gcc

EXPOSE 8000

ENTRYPOINT /app/docker/entrypoint
