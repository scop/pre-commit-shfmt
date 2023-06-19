# pre-commit-shfmt

[shfmt](https://github.com/mvdan/sh#shfmt) hook for
[pre-commit](https://pre-commit.com), with auto install.

Usage in `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/scop/pre-commit-shfmt
  rev: v3.6.0-2
  hooks:
    # Choose one of:
    - id: shfmt         # native (requires/installs Go to build)
    - id: shfmt-docker  # Docker image (requires Docker to run)
```
