# Sentieoslack

[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[black]: https://github.com/psf/black

## How to run locally

- To setup locally make sure `pyenv`, `Poetry`, and `nox` are installed

```bash
cd <project_directory>
```

- To create virtual environment and install development dependencies

```bash
make develop
```

- Run tests to ensure everything is setup

```bash
make test
```

## Project overview

### Files and directories

```bash
├── .cookiecutter.json                          # Cookiecutter attributes and values
├── .cruft.json                                 # Cruft info, used for updating project
├── .flake8                                     # Flake8 config
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml                     # Pre commit hooks
├── .vscode                 
│   ├── settings.json                           # Sample .vscode python setings
│   └── tasks.json                              # Test runner for VSCode unit test runner
├── Makefile                                    # Makefile to setup, test, and build the project
├── README.md   
├── noxfile.py                                  # Nox config file, defines test sessions
├── poetry.lock
├── pyproject.toml
├── src
│   └── sentieoslack
│       ├── __init__.py
│       └── py.typed                            # Marker file for PEP 561
└── tests                                       # Pytest unit tests
    ├── __init__.py
    └── test_main.py
```

## Makefile Usage


<details>
<summary>Setup development environment</summary>
<p>

To install run:

```bash
make develop
```

To uninstall

```bash
make delete-env && make cleanup
```

</p>
</details>


<details>
<summary>Codestyle</summary>
<p>

Automatic formatting uses `pyupgrade`, `isort` and `black`.

To check formatting issues run

```bash
make check-format
```

To auto fix formatting issue

```bash
make format
```

</details>

<details>
<summary>Code security</summary>
<p>

This command launches `Poetry` integrity checks as well as identifies security issues with `Safety` and `Bandit`.

```bash
make check-safety
```

</p>
</details>

<details>
<summary>Type checks</summary>
<p>

Run `mypy` static type checker

```bash
make check-static-type
```

Run `typeguard` run time type checker

```bash
make check-run-type
```

To run both together, run

```bash
make check-type
```

</p>
</details>

<details>
<summary>Tests with coverage report</summary>
<p>

Run `pytest`

```bash
make test
```

Run `nox` session to test package in multiple python versions

```bash
make test-all
```

</p>
</details>

<details>
<summary>Linting</summary>
<p>

To run `flake8` linting which will report issues

```bash
make check-issues
```

And to check for all linting, and typing, and safety issues

```bash
make check
```

</p>
</details>

<details>
<summary>Complexity</summary>
<p>

To generate code quality metric report using `radon` run

```bash
make code-metrics
```

</p>
</details>

<details>
<summary>Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>

## 🎯 What's next

Well, that's up to you 💪🏻. I can only recommend the packages to use

- [`Pydantic`](https://github.com/samuelcolvin/pydantic/) – data validation and settings management using Python type hinting.
- [`Loguru`](https://github.com/Delgan/loguru) makes logging (stupidly) simple.
- [`IceCream`](https://github.com/gruns/icecream) is a little library for sweet and creamy debugging.
- [`Returns`](https://github.com/dry-python/returns) makes you function's output meaningful, typed, and safe!
- [`Dynaconf`](https://github.com/rochacbruno/dynaconf) Configuration management for Python
- [`FastAPI`](https://github.com/tiangolo/fastapi) is a type-driven asynchronous web framework.

And stay up to date by following

- [`Awesome Python Feed`](https://python.libhunt.com/)

## Contributing

Contributions are very welcome.
