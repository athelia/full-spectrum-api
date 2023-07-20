# Full Spectrum API
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Purpose
Provide an API for Full Spectrum Eggs, a backyard farm ecommerce site.

## Prerequisites
- Install Python 3.10.10
  - Recommended: manage Python versions with `pyenv` - [pyenv github](https://github.com/pyenv/pyenv) 
  - Alternatively, you can [direct download 3.10.10](https://www.python.org/downloads/release/python-31010/)
- [Install `poetry` package manager](https://python-poetry.org/docs/#installation)
- Install PostGreSQL 14:
  - by [direct download](https://www.postgresql.org/download/)
  - or with Homebrew: `brew install postgresql@14`

## Installation
1. Clone repository to local directory
2. Create psql database `fullspectrum-dev`: 
```bash
createdb fullspectrum-dev
## below optional, but verifies db was created successfully
psql fullspectrum-dev
```
3. Run `model.py`. 
   - This will require db admin credentials. Usually, these match your user login credentials.
   - The file will create the tables and relationships.
4. Run `main.py`.
   - This starts the local server.
