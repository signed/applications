$packages = [ "curl", "git", "python", "python-setuptools", "python-virtualenv"]

package { $packages: ensure => installed }