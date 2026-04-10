# For development, [hatch](https://hatch.pypa.io/latest/why/) is used to manage the virtual environment and dependencies.

Make sure you have hatch installed in your default Python environment:

```bash
hatch --version
```

If it is not installed, you can install it using pip:

```bash
pip install hatch
```

# Development installation / activation
```bash
hatch shell
```

## Virtual Environment Setup

Hatch manages virtual environments for this project. Virtual environments can be stored in a centralized location by adding the following to `~/.config/hatch/config.toml`:

```toml
[envs]
storage.path = "~/_virtualenvs/hatch_envs"
```

This configuration centralizes all environments in one directory for easier management across projects.

To deactivate the environment, run:

```bash
exit
```

## Building Documentation

To generate HTML documentation, first activate the Hatch environment:

```bash
hatch shell
```

Then navigate to the docs folder and build the HTML files:

**On Windows:**
```bash
cd docs
./make.bat html
```

**On Linux/Mac:**
```bash
cd docs
make html
```

The generated HTML documentation will be available in `docs/build/html/`. Open `docs/build/html/index.html` in your browser to view the documentation.

## Tutorials

Tutorials are available in the `docs/source/notebooks` directory. To run a tutorial, activate the Hatch environment and execute the desired tutorial script:

```bash
hatch shell
```

Make sure you have Jupyter installed in the environment:

```bash
pip install jupyter
```

Then you can open the Jupyter Notebook interface by running:

```bash
jupyter notebook 
```

This will open a web interface where you can navigate to the `docs/source/notebooks` directory and open the tutorial notebooks to run them interactively.