#command to run salt states inside vagrant box
sudo apt-get install salt-minion
sudo salt-call --file-root=/vagrant/states --local state.highstate


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