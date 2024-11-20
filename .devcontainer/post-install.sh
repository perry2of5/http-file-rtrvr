#!/bin/bash
set -ex

##
## Create some aliases
##
echo 'alias ll="ls -alF"' >> $HOME/.bashrc
echo 'alias la="ls -A"' >> $HOME/.bashrc
echo 'alias l="ls -CF"' >> $HOME/.bashrc

# Convenience workspace directory for later use
WORKSPACE_DIR=$(pwd)

# Change some Poetry settings to better deal with working in a container
poetry config cache-dir ${WORKSPACE_DIR}/.cache
poetry config virtualenvs.in-project true

# Now install all dependencies
# poetry export --without-hashes --format=requirements.txt > requirements.txt
# pip install -r poetry export --without-hashes --format=requirements.txt
# rm requirements.txt

poetry config virtualenvs.in-project true --local
poetry install

echo "Done!"