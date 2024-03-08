# pre-commit-hadolint

[hadolint](https://github.com/hadolint/hadolint/) hook for
[pre-commit](https://pre-commit.com), with auto install.

Usage in `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/hadolint/hadolint/
  rev: v2.12.0
  hooks:
    - id: hadolint        # prebuilt upstream executable
```
