#command to run salt states inside vagrant box
sudo apt-get install salt-minion
sudo salt-call --file-root=/vagrant/states --local state.highstate



#salt terms#
## PyObjects ##

https://docs.saltstack.com/en/latest/ref/renderers/all/salt.renderers.pyobjects.html

those seem to be a better alternative to jinja templating

##  modules ##
I think comparable to puppet modules, but not sure