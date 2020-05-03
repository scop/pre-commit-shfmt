# pre-commit-shfmt-workaround

Temporary workaround for using shfmt with pre-commit <= 2.3.0. Usage:

```yaml
- repo: https://github.com/scop/pre-commit-shfmt-workaround
  rev: v0
  hooks:
    - id: shfmt
      name: shfmt
      language: golang
      additional_dependencies: [mvdan.cc/sh/v3/cmd/shfmt@v3.1.1]
      entry: shfmt
      args: [-w]
      types: [shell]
```

This will likely go away as soon as pre-commit > 2.3.0 is out; with
that it should be possible to use `local` instead of this as `repo`,
and `rev` removed.
