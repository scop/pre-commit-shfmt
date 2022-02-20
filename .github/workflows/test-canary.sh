#!/bin/sh
set -eu

# This script is fed to the hooks defined in this repo in CI for some
# basic smoke tests. It must not provoke any formatting changes or
# errors from shfmt.

echo "Hello, test."
