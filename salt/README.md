#command to run salt states inside vagrant box
sudo apt-get install salt-minion
sudo apt-get install  python-pygit2 #https://docs.saltstack.com/en/latest/topics/tutorials/gitfs.html
sudo salt-call --file-root=/vagrant/states --local state.highstate
sudo salt-call --file-root=/vagrant/states --config-dir=/vagrant  --local state.highstate -l debug


# next #
docker
https://github.com/saltstack-formulas/docker-formula
https://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html

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

## grains ##
As far as I understand those are basic facts gathered from the system

## pillar ##
A configuration mechanism?

