#!/usr/bin/env python3

import string
import sys

hooks_template = """
- id: hadolint
  name: hadolint
  description: Dockerfile linter
  language: python
  entry: hadolint
  types: [dockerfile]
  stages: [commit, merge-commit, push, manual]
"""


def main() -> None:
    # If you later decide to use a dynamic value, like Hadolint version, you can reintroduce and use a data dictionary here.
    hooks_yaml = hooks_template.strip()  # Use strip() if you want to remove leading/trailing whitespace for cleanliness.
    sys.stdout.write(hooks_yaml)

if __name__ == "__main__":
    main()
