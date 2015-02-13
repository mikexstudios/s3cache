name             's3cache'
version          '0.1.0'

supports 'ubuntu', '~> 14.04'
 
# These cookbooks are so common that we do not version pin them.
#%w{apt git user sudo ohai ssh_known_hosts}.each do |dep|
%w{apt}.each do |dep|
  depends dep
end

depends 'docker', '~> 0.36.0'
