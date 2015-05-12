# s3cache

s3cache is a drop-in proxy for Amazon's S3 that serves files from a local cache, 
when possible, to significantly reduce data transfer costs.

Older, less frequently accessed cached files are automatically expired when
disk space runs low. Built using nginx + gunicorn + flask, the entire proxy
runs in a single docker container for easy deployment. 

This project was inspired and guided by Akeem McLennon's
[docker-s3cache](https://github.com/AkeemMcLennon/docker-s3cache) with a [number
of differences](#differences).

## Getting started

The easiest way to try out s3cache locally is to use
[docker-compose](https://github.com/docker/compose): 

```bash
S3_ACCESS_KEY_ID=[access key] S3_SECRET_ACCESS_KEY=[secret key] \
  S3_BUCKET=[bucket name] docker-compose up
```

If you do not wish to use docker-compose, then you can manually run the
docker container:

```bash
docker pull mikexstudios/s3cache
docker run --env="S3_BUCKET=[bucket name]" \
           --env="S3_ACCESS_KEY_ID=[access key]" \
           --env="S3_SECRET_ACCESS_KEY=[secret key]" \
           --publish="80:80" \
           --volume="/tmp/s3cache:/usr/src/app/cache" \
           mikexstudios/s3cache
```

Once the container is running, visit that page in your web browser. You should
see a blank page. To use the proxy, simply change your S3 URL from (for example):

```
http://s3.amazonaws.com/bucketname/folder/file.ext?Signature=Xyj%2BMvilNgqLr67gF%2J97HDiJC%2Fs%3D&Expires=1423846845&AWSAccessKeyId=[some access key]`
```

to:

```
http://[servername]/bucketname/folder/file.ext?Signature=Xyj%2BMvilNgqLr67gF%2J97HDiJC%2Fs%3D&Expires=1423846845&AWSAccessKeyId=[some access key]`
```

You should receive the file as a download and see that it has been cached under
`/usr/src/app/cache`.


## Deployment

For production deployment, you may want to use the [included ansible
playbook](https://github.com/mikexstudios/s3cache/tree/master/ansible)
to automatically provision a server with docker, pull the s3cache image, and
run the container.


## How it works

TODO


## Differences

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
- ansible playbook is included to quickly bootstrap this app on any ubuntu-like
  server.

