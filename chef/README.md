## Testing chef deployment

We deploy s3cache by spinning up a Ubuntu server, installing docker, and then
pulling and running the `mikexstudios/s3cache` image from the docker hub.

To automate this process, we use a very minimal chef cookbook so that we can 
use `knife solo` to quickly run the cookbook on a remote server/node. However,
to test deployment locally, we turn to vagrant, which will spin up a full-fledged
Ubuntu virtual machine and run the chef cookbook. The steps are:

bundle install
berks vendor
S3_ACCESS_KEY_ID=[access key] S3_SECRET_ACCESS_KEY=[secret key] \
    S3_BUCKET=[bucket name] vagrant up
