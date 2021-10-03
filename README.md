# pre-commit-shfmt

[shfmt](https://github.com/mvdan/sh#shfmt) hook for
[pre-commit](https://pre-commit.com).

Usage in `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/scop/pre-commit-shfmt
  rev: v3.3.1
  hooks:
    # Choose one of:
    - shfmt         # native (requires Go to build)
    - shfmt-docker  # Docker image (requires Docker to run)
```
