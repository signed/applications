#!/usr/bin/env sh

sudo salt-call --local --config-dir=./salt/configuration --file-root=./salt/root --pillar-root=./salt/pillar state.highstate

