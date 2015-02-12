# s3cache

s3cache is a proxy for Amazon's S3 that caches files. Significant bandwidth costs
can be saved by serving S3 files locally. Older less frequenly accessed cached files
are automatically expired when disk space runs low. Built using nginx +
gunicorn + flask in a docker container for easy deployment.

This project was inspired and guided by Akeem McLennon's
[docker-s3cache](https://github.com/AkeemMcLennon/docker-s3cache). There are a 
few differences:

- URL scheme mirrors that of S3 such that the
  "http://[bucketname].s3.amazonaws.com/" part of the URLs can be directly
  replaced by the hostname of this proxy.
- This script was designed for GET links with Expires and Signature.
- Docker image is based off of
  [python:2.7-onbuild](https://registry.hub.docker.com/_/python/), which
  automatically installs from requirements.txt and copies app into the
  /usr/src/app folder.
- gunicorn + eventlet serves as the app runner instead of uwsgi. nginx is
  configured for gunicorn.
- [docker-compose/fig](https://github.com/docker/fig) is used for fast local
  development. gunicorn is set to hot reload the app server upon file change.
  The app folder is mounted as a volume in docker to reflect immediate file
  changes.
- python's multiprocessing module replaces threading to cache S3 files in the
  background.
- `fcntl.flock` is employed for file locking during background S3 file caching
  instead of `.lock` files. This is better since `.lock` files may not be 
  removed if the app crashes.
- cron job is used to expire old cached files instead of using a background 
  thread on each request.
- chef cookbook is included to quickly bootstrap this app on any ubuntu-like
  server.

## Getting started

TODO

## How it works

TODO
