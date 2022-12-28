# Contributing

## Documentation

To contribue to the documentation, all you need to do is update either mkdocs.yml (if you are making a change to the config) or add/modify files under docs/. The method of running make and mkdocs has been deprecated in favor of allowing GitHub Actions to do the work. Simply commit your changes to the main branch and watch automation do its thing.

### Documentation layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

### Commands for contributing to documentation (DEPRECATED)

- `make` - Sets up python3 virtual environment
- `source .venv/bin/active` - Activates python3 virtual environment
- `mkdocs build` - Build the documentation site.
- `mkdocs help` - Print this help message.
- `mkdocs gh-deploy` - Deploy documentation updates to gh-deploy branch
