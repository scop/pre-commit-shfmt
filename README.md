# pre-commit-shfmt

This fork by default enforces a configuration that roughly follows [Google style](https://google.github.io/styleguide/shellguide.html), following steps described [here](https://github.com/mvdan/sh/blob/master/cmd/shfmt/shfmt.1.scd#examples).

[shfmt](https://github.com/mvdan/sh#shfmt) hook for
[pre-commit](https://pre-commit.com), with auto install.

Usage in `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/scop/pre-commit-shfmt
  rev: v3.7.0-3
  hooks:
    # Choose one of:
    - id: shfmt         # prebuilt upstream executable
    - id: shfmt-src     # build from source (requires/installs Go to build)
    - id: shfmt-docker  # Docker image (requires Docker to run)
```

> #### Note
> From v3.7.0-2 on, the `shfmt` id points to the variant that uses a prebuilt
> upstream executable. The one that builds from source is available as
> `shfmt-src`.
