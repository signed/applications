#command to run salt states inside vagrant box
sudo apt-get install salt-minion
sudo salt-call --file-root=/vagrant/states --local state.highstate
