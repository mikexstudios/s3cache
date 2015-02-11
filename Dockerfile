# Pull base image.
FROM python:2.7-onbuild

# Install Nginx. 
RUN \ 
  echo "deb http://nginx.org/packages/debian/ wheezy nginx" >> \
    /etc/apt/sources.list.d/nginx.list && \
  apt-key adv --fetch-keys "http://nginx.org/keys/nginx_signing.key" && \
  apt-get update && \
  apt-get install -y nginx
EXPOSE 80 
EXPOSE 443 
# Define mountable directories.
VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs", "/etc/nginx/conf.d", "/var/log/nginx", "/var/www/html"]
# Copy nginx site config for gunicorn app

# A strange bug in fig somehow prevents the 'default' file from being overwritten
# with 'fig up' but works when 'fig run' or 'docker run' is used. So we copy
# the individual file over.
#COPY nginx/sites-enabled /etc/nginx/sites-enabled
COPY nginx/sites-enabled/default /etc/nginx/sites-enabled/default

# Install vim (good for debugging)
RUN apt-get install -y vim

EXPOSE 8000 
RUN mkdir /tmp/s3cache
VOLUME ["/usr/src/app", "/tmp/s3cache"] #for webapp
CMD nginx && gunicorn --config gunicorn.py.ini app:app
