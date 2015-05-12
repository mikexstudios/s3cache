# Deploying with ansible

We deploy s3cache by spinning up a Ubuntu server, installing docker, and then
pulling and running the `mikexstudios/s3cache` image from the docker hub.
To automate this process, we use a very minimal ansible playbook.

### Local testing

To test deployment locally, we turn to vagrant, which will spin up a
full-fledged Ubuntu virtual machine and run the ansible playbook. We do not
test through Docker since their Ubuntu images are stripped down and do not
perfectly mimic a VPS or dedicated server. The steps are:

1. Install [ansible](https://github.com/ansible/ansible). It is recommended to 
   use the HEAD branch of ansible since it includes many bugfixes:

   ```bash
   brew install --HEAD ansible
   ```

2. Pull in 3rd party playbooks that will be installed in `vendor/`:

   ```bash
   ansible-galaxy install -r requirements.yml
   ```

3. Make a copy of `vars/secrets.yml.example` and fill in the S3 API keys and
   bucket information:

   ```bash
   cd vars/
   cp secrets.yml.example secrets.yml
   vim secrets.yml #edit and fill in vars
   ```

4. Start vagrant:

   ```bash
   vagrant up
   ```

That's it! Whenever you make a change, you can simply reprovision vagrant by:
`vagrant provision`.


### Production deployment

Deployment to production is very similar except that ansible is called directly
instead of using vagrant.

1. Follow steps 1–3 from **local testing**.

2. Make a copy of `inventory.example` and fill in the default host. You may need
   to [set the ssh user and password or other options][1].

   ```bash
   cp inventory.example inventory
   vim inventory #edit and fill in
   ```

3. Run the playbook on the host (add `--check` to the command to perform a trial
   run without changing anything on the server):

   ```bash
   ansible-playbook -i inventory site.yml
   ```

[1]: http://docs.ansible.com/intro_inventory.html#list-of-behavioral-inventory-parameters

