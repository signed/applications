#!/usr/bin/env sh

sudo salt-call --local --config-dir=./configuration --file-root=./root --pillar-root=./pillar state.highstate

