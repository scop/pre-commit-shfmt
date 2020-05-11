# pre-commit-shfmt-workaround

Obsolete temporary workaround for using shfmt with pre-commit <= 2.3.0.

Upgrade to pre-commit >= 2.4.0 _now_, and use a config like the below,
except change to `repo: local` and remove `rev`. Or take backups or
fork this repo, if you want to keep using this, this one will go away
really soon now.

Usage:

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
