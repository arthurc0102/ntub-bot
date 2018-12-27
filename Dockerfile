# Create requirements.txt
FROM python:3.7

WORKDIR /app/src/

COPY Pipfile .
COPY Pipfile.lock .

RUN pip3 install --no-cache-dir pipenv
RUN pipenv lock -r > requirements.txt


# Django build
FROM alpine:3.8

# Change working directory
WORKDIR /usr/src/app

# Volumes
VOLUME /usr/src/app/log
VOLUME /usr/src/app/media
VOLUME /usr/src/app/assets

# Posts
EXPOSE 8000

# Install packages
RUN apk add --no-cache \
  python3 \
  python3-dev \
  linux-headers \
  gcc \
  musl-dev \
  postgresql-dev \
  libffi-dev \
  jpeg-dev \
  zlib-dev

# Copy docker-entrypoint.sh
COPY ./docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Update pip and setuptools
RUN pip3 install --upgrade --no-cache-dir pip setuptools uwsgi

# Copy Djnago project to working directory
COPY . .
COPY --from=0 /app/src/requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# Run!
ENTRYPOINT [ "docker-entrypoint.sh" ]
CMD [ "uwsgi", "--ini", "uwsgi.ini" ]
