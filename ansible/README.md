# Deploying with ansible

We deploy s3cache by spinning up a Ubuntu server, installing docker, and then
pulling and running the `mikexstudios/s3cache` image from the docker hub.
To automate this process, we use a very minimal ansible playbook.

### Local testing

To test deployment locally, we turn to vagrant, which will spin up a
full-fledged Ubuntu virtual machine and run the ansible playbook. We do not
test through Docker since their Ubuntu images are stripped down and do not
perfectly mimic a VPS or dedicated server. The steps are:

1. Pull in 3rd party playbooks:

   ```bash
   ansible-galaxy install -r requirements.yml
   ```

2. Start vagrant:

   ```bash
   S3_ACCESS_KEY_ID=[access key] S3_SECRET_ACCESS_KEY=[secret key] \
     S3_BUCKET=[bucket name] vagrant up
   ```

That's it! Whenever you make a change, you can simply reprovision vagrant by:
`vagrant provision`.
