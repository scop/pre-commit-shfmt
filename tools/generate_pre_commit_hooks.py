#!/usr/bin/env python3

import contextlib
import string
import sys

import docker


hooks_template = """
- id: shfmt
  name: shfmt
  description: Shell source code formatter (prebuilt upstream executable)
  language: python
  entry: shfmt
  args: [-w, -s]
  types: [shell]
  exclude_types: [csh, tcsh, zsh]
  stages: [pre-commit, pre-merge-commit, pre-push, manual]
  minimum_pre_commit_version: 3.2.0 # for "stages" names

- id: shfmt-src
  name: shfmt
  description: Shell source code formatter (build from source)
  language: golang
  # Note: keep Go version in `go.mod` in sync with shfmt's required Go version
  additional_dependencies: [mvdan.cc/sh/v3/cmd/shfmt@${shfmt_tag}]
  entry: shfmt
  args: [-w, -s]
  types: [shell]
  exclude_types: [csh, tcsh, zsh]
  stages: [pre-commit, pre-merge-commit, pre-push, manual]
  minimum_pre_commit_version: 3.2.0 # for "stages" names

- id: shfmt-docker
  name: shfmt
  description: Shell source code formatter (Docker image)
  language: docker_image
  # Note: use the top level multiplatform image digest here
  entry: --net none mvdan/shfmt:${shfmt_tag}@${docker_image_digest}
  args: [-w, -s]
  types: [shell]
  exclude_types: [csh, tcsh, zsh]
  stages: [pre-commit, pre-merge-commit, pre-push, manual]
  minimum_pre_commit_version: 3.2.0 # for "stages" names
"""


def main(python_pkg_tag: str) -> None:
    shfmt_tag, _, _ = python_pkg_tag.partition("-")

    with contextlib.closing(docker.from_env()) as client:
        registry_data = client.images.get_registry_data(f"mvdan/shfmt:{shfmt_tag}")

    # Top level multiplatform image digest
    docker_image_digest = registry_data.attrs["Descriptor"]["digest"]

    data = {
        "shfmt_tag": shfmt_tag,
        "docker_image_digest": docker_image_digest,
    }
    st = string.Template(hooks_template.lstrip())
    hooks_yaml = st.substitute(data)
    sys.stdout.write(hooks_yaml)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} PYTHON-PKG-TAG", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1])
