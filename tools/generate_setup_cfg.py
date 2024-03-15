#!/usr/bin/env python3

# Copyright 2023 Ville Skyttä
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import re
import string
import sys
from urllib.parse import quote as urlquote
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

setup_cfg_template = """
[metadata]
name = hadolint_py
version = ${python_pkg_version}
description = Dockerfile linter
url = https://github.com/scop/pre-commit-shfmt
# license here is for hadolint proper; Python packaging related files may have others, see their contents and classifiers below
license = GPL-3.0-only
classifiers =
    Intended Audience :: Developers
    License :: OSI Approved :: GNU General Public License v3 (GPLv3)
    Operating System :: MacOS
    Operating System :: Microsoft :: Windows
    Operating System :: POSIX :: Linux
    Programming Language :: Haskell
project_urls =
    Upstream = https://github.com/hadolint/hadolint

[options]
packages =
python_requires = >=3.8
setup_requires =
    setuptools-download

[setuptools_download]
download_scripts =
    [hadolint]
    group = hadolint-binary
    marker = sys_platform == "linux" and platform_machine == "aarch64"
    url = ${url_linux_arm64}
    sha256 = ${hexdigest_linux_arm64}
    [hadolint]
    group = hadolint-binary
    marker = sys_platform == "linux" and platform_machine == "x86_64"
    url = ${url_linux_amd64}
    sha256 = ${hexdigest_linux_amd64}
    [hadolint.exe]
    group = hadolint-binary
    marker = sys_platform == "win32" and platform_machine == "AMD64"
    marker = sys_platform == "cygwin" and platform_machine == "x86_64"
    url = ${url_windows_amd64}
    sha256 = ${hexdigest_windows_amd64}
"""

release_files = [
    # replace once the segfault issue is fixed for hadolint on github
    # "hadolint-Darwin-x86_64", 
    "hadolint-Linux-arm64",
    "hadolint-Linux-x86_64",
    "hadolint-Windows-x86_64.exe",
]

def fetch_checksum(binary_name, base_url):
    sha256_url = f"{base_url}{binary_name}.sha256"
    try:
        with urlopen(sha256_url) as response:
            content = response.read().decode('utf-8')
        checksum = content.split()[0]
        if not re.match(r'^[A-Fa-f0-9]{64}$', checksum):
            print(f"Invalid checksum for {binary_name}")
            return None
        return checksum
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
    except URLError as e:
        print(f"URL Error: {e.reason}")

HADOLINT_MACOS_SHA256 = "1ce867b213ba400ed1b7e04cdb1f1046513d16b901a1533cf1c58ba981a3061d"
# Adjustments made for macOS binary fetching from Homebrew
HADOLINT_MACOS_BOTTLE_URL = f"https://ghcr.io/v2/homebrew/core/hadolint/blobs/sha256:{HADOLINT_MACOS_SHA256}"


def main(python_pkg_tag: str) -> None:
    main_tag = python_pkg_tag  # Keep the "v" prefix as part of the version
    base_url = f"https://github.com/hadolint/hadolint/releases/download/{urlquote(main_tag)}/"

    data = {
        "python_pkg_version": main_tag,
        "url_darwin_amd64": HADOLINT_MACOS_BOTTLE_URL,
        "hexdigest_darwin_amd64": HADOLINT_MACOS_SHA256,
    }

    for binary in release_files:
        parts = binary.split('-')  # Splitting the binary name into parts, excluding 'hadolint'
        os_part, arch_part = parts[1], parts[2]
        if arch_part == "x86_64": arch_part = "amd64"  # Adjusting the architecture naming except for Windows
        if 'Windows' not in binary:
            os_arch = f"{os_part.lower()}_{arch_part}"  # Forming os_arch without the 'hadolint' prefix and adjusted architecture naming
        else:
            os_arch = "windows_amd64"
        binary_name = f"{binary}"
        checksum = fetch_checksum(binary_name, base_url)
        
        if checksum is None:
            print(f"Could not fetch checksum for {binary_name}. Skipping.")
            continue  # Skip this binary and continue with the next one
        
        data[f"url_{os_arch}"] = f"{base_url}{binary_name}"
        data[f"hexdigest_{os_arch}"] = checksum
    try:
        setup_cfg = string.Template(setup_cfg_template.lstrip()).substitute(data)
    except KeyError as e:
        print(f"Missing key in data dictionary: {e}")
        return
    sys.stdout.write(setup_cfg)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} PYTHON-PKG-TAG", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1])