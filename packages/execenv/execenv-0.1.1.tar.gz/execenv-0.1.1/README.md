[![License](https://img.shields.io/github/license/zyf722/execenv)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/execenv?logo=pypi&logoColor=white&label=PyPI)](https://pypi.org/project/execenv/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/execenv?logo=python&logoColor=white&label=Python)](https://pypi.org/project/execenv/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue?logo=python&logoColor=white)](https://mypy-lang.org/)
[![Github Actions Build](https://img.shields.io/github/actions/workflow/status/zyf722/execenv/build.yml?logo=github)](https://github.com/zyf722/execenv/actions/workflows/build.yml)
[![Code Coverage](https://img.shields.io/codecov/c/github/zyf722/execenv?logo=codecov&logoColor=white
)](https://app.codecov.io/github/zyf722/execenv/)

# execenv

Powered by [`click`](https://click.palletsprojects.com/), `execenv` is a simple cross-platform cli utility that allows you to execute commands with different environment variables by passing directly or loading from a `.env` file.

![Preview](./assets/preview.png)

Thanks to [`rich-click`](https://github.com/ewels/rich-click), it also supports rich output for a better user experience:

![Preview (rich)](./assets/preview-rich.png)

## Installation
### With `pipx`
> [!NOTE]
> `pipx` is a specialized package installer. It can only be used to install packages with cli entrypoints and help you to isolate the environment of each package.
>
> Check out the [official documentation](https://pipx.pypa.io/stable/comparisons/) to gain more insights.

As a cli application, it is recommended to install `execenv` via [`pipx`](https://github.com/pypa/pipx):

```shell
pipx install execenv
```

To enable rich output, use

```shell
pipx install execenv[rich]
```

### With `pip`
Alternatively, you can install `execenv` via `pip`:

```shell
pip install execenv

# Or with rich output
pip install execenv[rich]
```

### From Source
You might also want to install `execenv` from source.

This project uses [`poetry`](https://python-poetry.org/) for dependency management. Make sure you have it installed before proceeding.

```shell
git clone https://github.com/zyf722/execenv.git
cd execenv/

poetry lock
poetry install
```

After that, you can run the application with:

```shell
poetry run execenv
```

## Usage
This package contains three cli applications:
- `execenv`: The main application.
- `execenv-completion`: A completion utility to generate completion scripts for other shells.
- `execenv-echo`: A simple application for testing, which prints out K-V pairs of all given environment variables.

### Basic Usage
#### `-e` / `--env`
To run command with specific environment variables, you can pass them directly using the `-e` / `--env` flag:

```shell
execenv -e SHELL overwritten -e KEY VAL -- execenv-echo SHELL KEY

# Or put command before options
execenv execenv-echo SHELL KEY -e SHELL overwritten -e KEY VAL

# Output
# SHELL=overwritten
# KEY=VAL
```

#### `-f` / `--file`
Or you can load K-V pairs from a `.env` file ([dotenv compatible syntax](https://www.npmjs.com/package/dotenv#what-rules-does-the-parsing-engine-follow)) using the `-f` / `--file` flag:

```shell
execenv -f .env -- execenv-echo KEY

# Output
# KEY=VAL
```

#### `-c` / `--clear`
By default, current environment variables will be preserved. You can override this behavior by using the `-c` / `--clear` flag:

```shell
execenv -c -- set

# Output differs on different platforms
#
# Note that for Windows with Python 3.10 and earlier,
# this command might not work as expected with an error with `CreateProcess`
# Check python/cpython#105436 for further information 
```

> [!NOTE]
> The apply order of environment variables is as follows:
> 
> - Existing environment variables, if not cleared with `-c` / `--clear` flags
> - Variables loaded from `.env` file with `-f` / `--file` flags
> - `-e` / `--env` flags
>
> Variables with the same key will be overwritten by the latter ones.
> 
> For those on the same level, the order of appearance in the command line will be followed.

#### `-a` / `--append-env` & `--append-separator`
Use `-a` / `--append-env` to append value to variables instead of overwriting:

```shell
execenv -e KEY VAL -a KEY test -- execenv-echo KEY

# Output
# KEY=VAL;test (on Windows)
# KEY=VAL:test (on Linux / macOS)

# Also works with existing ones
execenv -a PATH test -- execenv-echo PATH

# Output
# PATH=%PATH%;test (on Windows)
# PATH=$PATH:test (on Linux / macOS)
```

By default `os.pathsep` is used as the separator when appending. You can change it by using `--append-separator` flag:

```shell
execenv --append-separator . -a KEY test -e KEY VAL -- execenv-echo KEY

# Output
# KEY=VAL.test
```

> [!WARNING]
> Be cautious when setting the separator to special characters like `|` with `-s` / `--shell` flag, as they might be misinterpreted by the shell, or even lead to security vulnerabilities.

### Shell Related
#### `-s` / `--shell`
Use `-s` / `--shell` to set `shell=True` to `subprocess` in order to use expansion, built-in commands, pipes, redirection and other shell features:

```shell
# Linux / macOS
execenv -e PATH overwritten -e KEY VAL -s -- echo EXECENV_PATH \$KEY

# Windows
execenv -e PATH overwritten -e KEY VAL -s -- echo EXECENV_PATH %KEY%

# Output
# overwritten VAL
```

> [!TIP]
> You should escape `$` on Linux / macOS using `\` and `%` on Windows using `^` to prevent them from being expanded by the shell if you want to use new values set with `execenv`.
>
> Alternatively, you can use a prefix to access them. By default, `EXECENV_` is used as the prefix. You can change it by using `--env-varref-prefix` flag.

> [!WARNING]
> You should be cautious when using `shell=True` as it might lead to [security vulnerabilities](https://docs.python.org/3/library/subprocess.html#security-considerations). Make sure you trust the input and the command you are running.
>
> On POSIX platforms, due to features like expansion can not work with `shlex.join` as they are escaped for security reasons, internally `subprocess.list2cmdline` is used by default, which is less secure and compatible with POSIX. You can change it by using `--shell-strict` flag to switch back to `shlex.join`.

#### `-C` / `--cwd`
Use `-C` / `--cwd` to set the working directory, and note that `-s` / `--shell` is not mandatory to use this option:

```shell
# Linux / macOS
execenv -C /home -- pwd

# Windows
execenv -C C:\ -s -- echo EXECENV_CD

# Output
# C:\ (on Windows)
# /home (on Linux / macOS)
```

### Miscellaneous
#### `-h` / `--help`
Use `-h` / `--help` to get help information:

```shell
execenv -h

# Or simply without any flags and arguments
execenv
```

#### `-V` / `--version`
Use `-V` / `--version` to get the version information.

#### `-v` / `-vv` / `--verbose`
Use `-v` / `-vv` / `--verbose` to enable verbose mode, which is useful for debugging:

```shell
execenv -e SHELL overwritten -e KEY VAL -v -- execenv-echo SHELL KEY
```

![Verbose](./assets/verbose.png)

A header section will be added to the output to show details about `execenv` itself. Use `-vv` to show more information.

#### `--config`
Use `--config` to load configuration from a file. Note that config file itself is [a valid `.env` file](#-f----file).

Default config file will be created after the first run at `~/.execenv.env` on Linux / macOS and `%USERPROFILE%\.execenv.env` on Windows.

Refer to [`execenv/config.py`](./execenv/config.py) to see all available configuration with their default values.

### Auto Completion
#### Click Built-in Shells (Bash 4.4+, Zsh & Fish)
For [shells supported by `click`](https://click.palletsprojects.com/en/8.1.x/shell-completion/), `execenv` will automatically setup tab completion after the first run (screenshot below is for Fish):

![Auto Completion (fish)](./assets/auto-completion-fish.png)

You may restart or source your shell to enable the completion.

#### Other Shells
A completion utility `execenv-completion` will also be installed with `execenv`. You can use it to generate completion scripts for other shells:

![execenv-completion](./assets/execenv-completion.png)

##### Clink (Windows `cmd`)
`execenv-completion` provides support for [clink](https://github.com/chrisant996/clink).

![Auto Completion (clink)](./assets/auto-completion-clink.png)

You can install it by running:

```shell
execenv-completion -s clink [-p /path/to/your/script]
```

It will create a `completions` directory in the specified path (or the current directory if not provided) with the completion `.lua` script inside.

> [!NOTE]
> Check out related [documentation](https://chrisant996.github.io/clink/clink.html#completion-directories) of `clink` for more information.

## Contributing

[Pull Requests](https://github.com/zyf722/execenv/pulls) are welcome!

It is strongly recommended to follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification when writing commit messages and creating pull requests.

## License
[MIT](./LICENSE)
