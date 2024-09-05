# Loci CLI Tool and Client Library
The official Loci CLI tool and Python client library. The CLI tool performs basic Loci Notes tasks from any command line, and the Python library can be used to build other Python clients.

**IMPORTANT: LOCI NOTES AS A WHOLE IS UNDERGOING REFACTORING, USE THE VERSION SPECIFIED BELOW TO MAKE SURE EVERYTTHING WORKS TOGETHER** 

## Docs
https://loci-notes.gitlab.io/clients/cli

## Installation
### Standard
`pip install loci-cli`

### Latest
#### Remote
`pip install git+https://gitlab.com/loci-notes/loci-cli`

#### Local
`git clone https://gitlab.com/loci-notes/loci-cli && pip install loci-cli`

### Development
```bash
pip install poetry
poetry config virtualenvs.in-project true
poetry install --with dev
poetry run loci --help
```

Use VS Code for development and debugging.
