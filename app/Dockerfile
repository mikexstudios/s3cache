# Pull base image.
FROM python:2.7-onbuild

# Install cron for expiring old cached files
# RUN apt-get install -y cron 
# COPY conf/cron/run_expire_cache /etc/cron.d/run_expire_cache

# app
EXPOSE 8000 
VOLUME ["/usr/src/app"]
# Disable print buffering in gunicorn for better development.
ENV PYTHONUNBUFFERED True
#TODO: Use a proper init system for running multiple programs in container
# CMD nginx && cron && gunicorn --config gunicorn.py.ini app:app
CMD ["gunicorn", "--config", "gunicorn.py.ini", "app:app"]
