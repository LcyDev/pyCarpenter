#!/bin/bash

# Set console title (optional, may not work in all terminals)
printf "\033]0;Loading Wood Rewritten...\007"

# Construct path to executable
path=$(dirname "$0")/libraries/Wood.exe

# Run the executable
"$path"
