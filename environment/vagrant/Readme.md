sudo useradd fump -m -s /bin/bash
sudo passwd fump
sudo usermod -a -G sudo fump


http://exponential.io/blog/2015/02/10/install-virtualenv-and-virtualenvwrapper-on-ubuntu/
http://stackoverflow.com/questions/34474606/setting-up-saltstack-for-local-masterless-development

sudo apt-get install libffi-dev

http://www.pygit2.org/install.html#libgit2-within-a-virtual-environment
sudo apt-get install libgit2-dev
pip install 'pygit2==0.22.1' --upgrade
#versions have to match
dpkg --get-selections | grep libgit
http://www.pygit2.org/install.html