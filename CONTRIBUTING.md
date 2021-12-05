# Contribution Guide

## Install poetry
Poetry is a `pip` replacement that also handles virtual environments, dependency updates, building, packaging, and publishing. It uses `pyproject.toml` (the recommended project configuration file by the community) for configuration and provides a nice user interface.

See [Poetry Installation Page](https://python-poetry.org/docs/#installation) to download and install a self contained Poetry instance with vendorized dependencies for complete isolation from the rest of the system. You can run these tools manually, or use pre-commit (see below).

## Install dependencies
Currently there are only development dependencies. These dependencies are not distributed with the package when it is published. Instead, we use them to ensure code quality. The coding style used in this project mostly conforms to [Google Style Guide](https://google.github.io/styleguide/pyguide.html), except for line length (88) and some naming exceptions.

You are ready to work on the project!

**NOTE:** `pygame` did not work on Deniz's NixOS Linux computer. It worked fine on Yiğit's M1 MacBook. Please let us know if `pygame` does not work on your computer.

## See examples
While Poetry shell is active (check `$PS1`), you can run example files to see your changes. To do so: `$ python test_X.py`.

## Install precommit hooks
**This is only required if you are commit changes to the project.** Pre-commit tool installs hooks described in `.pre-commit-config.yaml` as precommit hooks. These hooks are used to check code quality before committing the changes you have made in the project. To install the hooks run `$ pre-commit install`. To manually execute the hooks run `$ pre-commit run`.
