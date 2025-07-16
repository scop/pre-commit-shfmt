# pre-commit-shfmt

[![Main push and PR checks](https://github.com/scop/pre-commit-shfmt/actions/workflows/check.yml/badge.svg)](https://github.com/scop/pre-commit-shfmt/actions/workflows/check.yml)
[![Tag checks](https://github.com/scop/pre-commit-shfmt/actions/workflows/check-tag.yml/badge.svg)](https://github.com/scop/pre-commit-shfmt/actions/workflows/check-tag.yml)
[![CodeQL](https://github.com/scop/pre-commit-shfmt/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/scop/pre-commit-shfmt/actions/workflows/github-code-scanning/codeql)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/scop/pre-commit-shfmt/badge)](https://scorecard.dev/viewer/?uri=github.com%2Fscop%2Fpre-commit-shfmt)

[shfmt](https://github.com/mvdan/sh#shfmt) hook for
[pre-commit](https://pre-commit.com), with auto install.

Usage in `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/scop/pre-commit-shfmt
  rev: v3.12.0-2
  hooks:
    # Choose one of:
    - id: shfmt         # prebuilt upstream executable
    - id: shfmt-src     # build from source (requires/installs Go to build)
    - id: shfmt-docker  # Docker image (requires Docker to run)
```

> #### Notes
>
> From v3.12.0-2 on, the default args passed to `shfmt`
> [no longer contain `-s`](https://github.com/mvdan/sh/issues/1173).
>
> From v3.7.0-2 on, the `shfmt` id points to the variant that uses a prebuilt
> upstream executable. The one that builds from source is available as
> `shfmt-src`.
