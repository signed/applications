#!/usr/bin/env sh

salt_command=`which salt-call`

sudo ${salt_command} --local --config-dir=./configuration --file-root=./root --pillar-root=./pillar state.highstate