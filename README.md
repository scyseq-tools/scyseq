# Development installation / activation

```bash
hatch shell
```

My own configuration uses a specific virtual environment per project:

env = "~/_virtualenvs/hatch_envs" is set in ~/.config/hatch/config.toml

and

```bash
exit
```

# Tools used in this package:

[sphinx](https://www.sphinx-doc.org) for the documentation

[pytest](https://docs.pytest.org) for testing

[hatch](https://hatch.pypa.io) for project management

[doctest](https://docs.python.org/3/library/doctest.html) for inserting tests in
docstrings
