FROM danielquinn/django:debian

COPY /requirements.txt /app/requirements.txt

# Install build dependencies
RUN apt update && \
  apt install -y gcc libffi-dev && \
  pip install -r /app/requirements.txt && \
  apt remove -y gcc && \
  apt autoremove -y

EXPOSE 8000

ENTRYPOINT /app/docker.entrypoint
