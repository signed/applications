#!/usr/bin/env sh
salt_command=`which salt-call`
root_directory=`pwd`

sudo ${salt_command} --local --config-dir=${root_directory}/salt/configuration --file-root=${root_directory}/salt/root --pillar-root=${root_directory}/salt/pillar state.highstate