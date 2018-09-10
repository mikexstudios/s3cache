# Pull base image.
FROM python:2.7-onbuild

# Install cron for expiring old cached files
RUN apt-get update \
      && apt-get install -y cron  \
      && rm -rf /var/lib/apt/lists/*
COPY cron/run_expire_cache /etc/cron.d/run_expire_cache

# app
EXPOSE 8000 
VOLUME ["/usr/src/app"]
# Disable print buffering in gunicorn for better development.
ENV PYTHONUNBUFFERED True
#TODO: Use a proper init system for running multiple programs in container
CMD cron && gunicorn --config gunicorn.py.ini app:app
