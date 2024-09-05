#!/usr/bin/env bash

# This script is used in testing.
# Can run directly or refer to in ".config/autostart/..." configuration.
# Copy it to "~/.local/bin"  See 
#   https://man7.org/linux/man-pages/man7/file-hierarchy.7.html
#    (search for local/bin)
#

# cd so that log files end up in home directory
cd ~

# Activate the environment it's installed in.
. ~/Documents/magic-lantern/.venv/bin/activate


# Two options: 
#    - run as a module with environment variable to profile
#    - run directly 

export MAGIC_LANTERN_PROFILE=1
#python -m magic_lantern "$@"
magic-lantern 

