#!/bin/bash

# This script is used to update the version number in the config.json file
# during the Docker build process in GitHub Actions.
# It replace latest in program arguments with current version of container.
# It also replaces the version number in the config.json file.

# Check if an argument is provided
if [ -z "$1" ]; then
    echo "No argument provided. Usage: ./update_version.sh <argument>"
    exit 1
fi

# Check if the input is "latest"
if [ "$1" == "latest" ]; then
    echo "Input is 'latest'. No changes made."
    exit 0
fi

version=$1

echo "Version: ${version}"


# constants.py
# Check if constants.py exists
if [ ! -f "src/constants.py" ]; then
    echo "File constants.py does not exist."
    exit 1
fi

# Replace "v0.0.0" in constants.py with the provided argument
sed -i.bak "s|v\.0\.0|${version}|g" src/constants.py && rm src/constants.py.bak

echo "Replaced 'v0.0.0' with '${version}' in src/constants.py."


# README.md
# Check if README.md exists
if [ ! -f "README.md" ]; then
    echo "File README.md does not exist."
    exit 1
fi

# Replace "latest" with the provided argument in README.md
sed -i.bak "s|:latest|:${version}|g" README.md && rm README.md.bak

echo "Replaced all occurrences of 'latest' with '${version}' in README.md."
