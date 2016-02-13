#command to run salt states inside vagrant box
sudo apt-get install salt-minion
sudo apt-get install  python-pygit2 #https://docs.saltstack.com/en/latest/topics/tutorials/gitfs.html
sudo salt-call --local --config-dir=/vagrant/salt/configuration --file-root=/vagrant/salt/root --pillar-root=/vagrant/salt/pillar -l debug <call>

## calls ##
* state.highstate
* pillar.data
* pillar.raw
* pillar.get <key>
* grains.items --output=pprint
* sys.doc


# next #
## how to write salt states
https://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html

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

## modules ##
There are significant differences between execution modules and state modules. Unfortunately the term module is a bit overloaded.

### state module ###
A state module tells the Salt Minion what the end result, or "state" should be.
Examples would be "make sure apache is installed" or "make sure this specific config file exists on the filesystem".
The important difference is that a state module will check the system to see if the machine conforms with the desired state before doing anything.
So in the case of "make sure apache is installed" the Salt Minion will check to see if Apache is installed and do nothing if Apache is installed.
If it's not obvious, Salt will install Apache if needed.

The state module should only perform "before" and "after" checks [link][state module]. 

[state module]: https://docs.saltstack.com/en/latest/ref/states/writing.html#full-state-module-example

### execution modules ###
An execution module is a command sent to a Salt Minion to be executed immediately. Examples are "install apache" or "restart memcached".

## debugging ##

https://docs.saltstack.com/en/latest/ref/modules/all/salt.modules.test.html