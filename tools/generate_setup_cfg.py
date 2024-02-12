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
from urllib.parse import quote as urlquote, urljoin
from urllib.request import urlopen

setup_cfg_template = """
[metadata]
name = shfmt_py
version = ${python_pkg_version}
description = Shell source code formatter
url = https://github.com/scop/pre-commit-shfmt
# license here is for shfmt proper; Python packaging related files may have others, see their contents and classifiers below
license = BSD 3-Clause
classifiers =
    Intended Audience :: Developers
    License :: OSI Approved :: Apache Software License
    License :: OSI Approved :: BSD License
    License :: OSI Approved :: MIT License
    Operating System :: MacOS
    Operating System :: Microsoft :: Windows
    Operating System :: POSIX :: Linux
    Programming Language :: Go
project_urls =
    Upstream = https://github.com/mvdan/sh#shfmt

[options]
packages =
python_requires = >=3.8
setup_requires =
    setuptools-download

[setuptools_download]
download_scripts =
    [shfmt]
    group = shfmt-binary
    marker = sys_platform == "darwin" and platform_machine == "x86_64"
    url = ${url_darwin_amd64}
    sha256 = ${hexdigest_darwin_amd64}
    [shfmt]
    group = shfmt-binary
    marker = sys_platform == "darwin" and platform_machine == "arm64"
    url = ${url_darwin_arm64}
    sha256 = ${hexdigest_darwin_arm64}
    [shfmt]
    group = shfmt-binary
    # TODO: verify i386
    marker = sys_platform == "linux" and platform_machine == "i386"
    marker = sys_platform == "linux" and platform_machine == "i686"
    url = ${url_linux_386}
    sha256 = ${hexdigest_linux_386}
    [shfmt]
    group = shfmt-binary
    marker = sys_platform == "linux" and platform_machine == "x86_64"
    url = ${url_linux_amd64}
    sha256 = ${hexdigest_linux_amd64}
    [shfmt]
    group = shfmt-binary
    # TODO: verify armv6hf
    marker = sys_platform == "linux" and platform_machine == "armv6hf"
    marker = sys_platform == "linux" and platform_machine == "armv7l"
    url = ${url_linux_arm}
    sha256 = ${hexdigest_linux_arm}
    [shfmt]
    group = shfmt-binary
    marker = sys_platform == "linux" and platform_machine == "aarch64"
    url = ${url_linux_arm64}
    sha256 = ${hexdigest_linux_arm64}
    [shfmt.exe]
    group = shfmt-binary
    # TODO: verify both
    marker = sys_platform == "win32" and platform_machine == "x86"
    marker = sys_platform == "cygwin" and platform_machine == "i386"
    url = ${url_windows_386}
    sha256 = ${hexdigest_windows_386}
    [shfmt.exe]
    group = shfmt-binary
    marker = sys_platform == "win32" and platform_machine == "AMD64"
    marker = sys_platform == "cygwin" and platform_machine == "x86_64"
    url = ${url_windows_amd64}
    sha256 = ${hexdigest_windows_amd64}
"""

release_files = [
    "shfmt_{main_tag}_darwin_amd64",
    "shfmt_{main_tag}_darwin_arm64",
    "shfmt_{main_tag}_linux_386",
    "shfmt_{main_tag}_linux_amd64",
    "shfmt_{main_tag}_linux_arm",
    "shfmt_{main_tag}_linux_arm64",
    "shfmt_{main_tag}_windows_386.exe",
    "shfmt_{main_tag}_windows_amd64.exe",
]


def main(python_pkg_tag: str) -> None:
    main_tag, _, _ = python_pkg_tag.partition("-")
    base_url = f"https://github.com/mvdan/sh/releases/download/{urlquote(main_tag)}/"

    data = {
        "python_pkg_version": python_pkg_tag.lstrip("v"),
    }
    url = urljoin(base_url, "sha256sums.txt")
    hexdigests = {}
    with urlopen(url) as f:
        for line in f:
            if m := re.search(r"^([0-9a-f]{64})\s+(\S+)$", line.decode()):
                hexdigests[m.group(2)] = m.group(1)
    for fn in release_files:
        if m := re.search(r"_([a-z0-9]+_[a-z0-9]+)(?:\.exe)?$", fn):
            os_arch = m.group(1)
        else:
            raise ValueError(f"could not determine OS/arch from {fn}")
        fn = fn.format(main_tag=main_tag)
        data[f"url_{os_arch}"] = urljoin(base_url, urlquote(fn))
        if hexdigest := hexdigests.get(fn):
            data[f"hexdigest_{os_arch}"] = hexdigest
        else:
            raise KeyError(f"no hexdigest found for {fn}")

    st = string.Template(setup_cfg_template.lstrip())
    setup_cfg = st.substitute(data)
    sys.stdout.write(setup_cfg)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} PYTHON-PKG-TAG", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1])
