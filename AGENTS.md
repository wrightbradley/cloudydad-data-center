# Build/Lint/Test Commands

- `make lint` - Run all linters via pre-commit
- `make pre-commit` - Run pre-commit hooks manually
- `make test` - Run tests (currently no test framework configured)
- `make docs` - Build and serve documentation site
- `make site` - Deploy full data center via Ansible
- `make reset` - Reset Kubernetes cluster
- `make install` - Install all dependencies (pip + galaxy)

# Code Style Guidelines

- YAML: 2-space indentation, 120 char line length, yamlfmt for formatting
- Python: 4-space indentation, single quotes for strings
- Shell: shellcheck for linting (excludes scripts/ and motd.d/)
- Ansible: Use FQCN modules (ansible.builtin.*), var-naming without role
  prefixes
- General: LF line endings, trim trailing whitespace, final newlines required
- Markdown: 80 char wrap, prose wrap always
- Pre-commit hooks enforce: trailing whitespace, YAML formatting, secret
  detection
