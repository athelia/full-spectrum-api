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
1. Clone repository to local directory.
2. Create psql database `fullspectrum-dev`:
    ```bash
    createdb fullspectrum-dev
    ```
    - Optionally, run `psql fullspectrum-dev` to verify that the database was created successfully.
    - If the above step fails, you may need to finish installing and starting postgres with:
        ```bash
        sudo mkdir -p /usr/local/pgsql/data
        sudo chown <your-username-here> /usr/local/pgsql /usr/local/pgsql/data  
        initdb -D /usr/local/pgsql/data
        pg_ctl -D /usr/local/pgsql/data -l logfile start
        ```
3. Run `poetry install` inside the project directory to install dependencies.
4. Run `poetry shell` to create and activate a shell within the virtual environment.
5. Run `model.py`. 
   - This may require db admin credentials. Usually, these match your user login credentials.
   - The file will create the tables and relationships.
6. Run `main.py`.
   - This starts the local server.
