#!/bin/sh
set -eu

# This script is fed to the hooks defined in this repo in CI for a
# basic smoke test. It must not provoke any formatting changes or
# errors from shfmt.

echo "Hello, test."
