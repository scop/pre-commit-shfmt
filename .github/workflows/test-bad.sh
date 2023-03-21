#!/bin/sh
set -eu

# This script is fed to the hooks defined in this repo in CI for a
# basic smoke test. shfmt is expected to make changes to it.

if true; then
echo "Hello, test."
fi
