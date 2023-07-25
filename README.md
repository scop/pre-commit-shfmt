# pre-commit-shfmt

[shfmt](https://github.com/mvdan/sh#shfmt) hook for
[pre-commit](https://pre-commit.com), with auto install.

Usage in `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/scop/pre-commit-shfmt
  rev: v3.7.0-1
  hooks:
    # Choose one of:
    - id: shfmt         # native (requires/installs Go to build)
    - id: shfmt-gstyle  # native, following a style close to that of Google's
    - id: shfmt-docker  # Docker image (requires Docker to run)
```

The `gstyle` variant follows configuration described [here](https://github.com/mvdan/sh/blob/master/cmd/shfmt/shfmt.1.scd#examples).
