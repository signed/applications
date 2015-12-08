#command to run salt states inside vagrant box
sudo apt-get install salt-minion
sudo apt-get install  python-pygit2 #https://docs.saltstack.com/en/latest/topics/tutorials/gitfs.html
sudo salt-call --local --file-root=/vagrant/salt/root --pillar-root=/vagrant/salt/pillar state.highstate
sudo salt-call --local --config-dir=/vagrant --file-root=/vagrant/salt/root --pillar-root=/vagrant/salt/pillar state.highstate -l debug


# next #
## salt best practices ##
https://docs.saltstack.com/en/latest/topics/best_practices.html

## learn how to write formulas #
https://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html

## salt can install itself with salt ##
https://github.com/saltstack-formulas/salt-formula

# open issues #
## ensure public keys are not tempered with ##
when adding a repository the finger print of the downloaded public key should be checked before the key is installed.

#salt terms#
## PyObjects ##

https://docs.saltstack.com/en/latest/ref/renderers/all/salt.renderers.pyobjects.html

those seem to be a better alternative to jinja templating

##  modules ##
I think comparable to puppet modules, but not sure
Right now I thing formulas are like puppet modules and the unit of sharing custom modules
https://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html

## formula ##
This seems the unit if sharing installation instructions with the community
A formula can be configured with a pillar

### including formula from git repositories ###
This needs to be configured in the `minion` file.

    fileserver_backend:
      - git


There can be other fileserver backends configured besides `git` like `roots` what is the default.
`salt-call` will clone the repositories into a subdirectory of `/var/cache/salt/minion/gitfs/` and keep track of the checkout hash at `/var/cache/salt/minion/gitfs/remote_map.txt`.
 
## grains ##
As far as I understand those are basic facts gathered from the system

## pillar ##
A configuration mechanism?

