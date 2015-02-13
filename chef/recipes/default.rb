# Cookbook deps
%w{apt}.each do |dep|
  include_recipe dep
end

# Install docker
include_recipe 'docker'

# Pull and run s3cache image from docker hub
docker_image 'mikexstudios/s3cache'
docker_container 'mikexstudios/s3cache' do
  # NOTE: An init script will be automatically created for this container.
  detach true #detach from container when starting
  port '80:80'
  volume '/tmp/s3cache/:/usr/src/app/cache'
  env ["S3_BUCKET=#{node['s3cache'].fetch('S3_BUCKET')}", 
       "S3_ACCESS_KEY_ID=#{node['s3cache'].fetch('S3_ACCESS_KEY_ID')}",
       "S3_SECRET_ACCESS_KEY=#{node['s3cache'].fetch('S3_SECRET_ACCESS_KEY')}"]
  action :run
end
