# Pull base image.
FROM python:2.7-onbuild

# Install Nginx: https://github.com/nginxinc/docker-nginx/blob/master/Dockerfile
RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62
RUN echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list
ENV NGINX_VERSION 1.9.0-1~jessie
RUN apt-get update && \
    apt-get install -y ca-certificates nginx=${NGINX_VERSION}
# forward request and error logs to docker log collector
# NOTE: Does not seem to work with running nginx in the background.
#RUN ln -sf /dev/stdout /var/log/nginx/access.log
#RUN ln -sf /dev/stderr /var/log/nginx/error.log
VOLUME ["/var/cache/nginx"]
EXPOSE 80 443

# Copy nginx site config for gunicorn app
COPY conf/nginx/nginx.conf /etc/nginx/nginx.conf
COPY conf/nginx/app.conf /etc/nginx/conf.d/default.conf
#COPY nginx/sites-enabled/default /etc/nginx/sites-enabled/default

# Install cron for expiring old cached files
RUN apt-get install -y cron 
COPY conf/cron/run_expire_cache /etc/cron.d/run_expire_cache

# Install vim for troubleshooting
RUN apt-get install -y vim-tiny 

# Clean apt cache
RUN rm -rf /var/lib/apt/lists/*

# app
EXPOSE 8000 
RUN mkdir /tmp/s3cache
VOLUME ["/usr/src/app", "/tmp/s3cache"] #for webapp
#TODO: Use a proper init system for running multiple programs in container
CMD nginx && cron && gunicorn --config gunicorn.py.ini app:app
