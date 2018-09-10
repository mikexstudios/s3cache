# s3cache

s3cache is a drop-in proxy for Amazon's S3 that serves files from a local cache, 
when possible, to significantly reduce data transfer costs.

Older, less frequently accessed cached files are automatically expired when
disk space runs low. Built using Caddy + gunicorn + flask, the entire proxy
runs with a single docker-compose command for easy deployment. 

## Usage

1. Set up environment variables in `.env`. An example environment file is 
   provided. To use, rename `.env.example` to `.env` and fill out the blanks.

2. Run the stack with docker-compose:
   
   ```
   docker-compose up
   ```

3. Once the container is running, visit that page in your web browser. You
   should see a blank page. To use the proxy, simply change your S3 URL from
   (for example):

   ```
   http://s3.amazonaws.com/bucketname/folder/file.ext?Signature=Xyj%2BMvilNgqLr67gF%2J97HDiJC%2Fs%3D&Expires=1423846845&AWSAccessKeyId=[some access key]`
   ```

   to:

   ```
   http://[servername]/bucketname/folder/file.ext?Signature=Xyj%2BMvilNgqLr67gF%2J97HDiJC%2Fs%3D&Expires=1423846845&AWSAccessKeyId=[some access key]`
   ```

   You should receive the file as a download and see that it has been cached under
   `/usr/src/app/cache`.

## How it works

When the S3 file is first sent to s3cache, the user is redirected to the actual
S3 URL while s3cache fetches the file in the background. When the file exists
on disk, then subsequent requests are served from the cache instead of hitting
S3. When the disk grows above 90% full, older files are deleted.

## Credits

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
- gunicorn + eventlet serves as the app runner instead of uwsgi. Caddy is
  configured for gunicorn.
- docker-compose is used for fast local development. gunicorn is set to hot
  reload the app server upon file change. The app folder is mounted as a volume
  in docker to reflect immediate file changes.
- python's multiprocessing module replaces threading to cache S3 files in the
  background.
- `fcntl.flock` is employed for file locking during background S3 file caching
  instead of `.lock` files. This is better since `.lock` files may not be 
  removed if the app crashes.
- cron job is used to expire old cached files instead of using a background 
  thread on each request.