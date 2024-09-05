import os
import platform
import re
import shlex
import subprocess
import sys
from functools import partial
from importlib.metadata import metadata
from io import TextIOWrapper
from pathlib import Path
from textwrap import dedent, indent
from types import TracebackType
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union, cast

# Optional rich feature
try:
    import rich_click as click  # type: ignore
    from rich.highlighter import ReprHighlighter
    from rich_click import rich_config

    help_config = click.RichHelpConfiguration(highlighter=ReprHighlighter())

except ImportError:
    import click  # type: ignore

    def rich_config(help_config: None):  # type: ignore
        def decorator(f: Callable) -> Callable:
            return f

        return decorator

    help_config = None  # type: ignore


from auto_click_auto import enable_click_shell_completion  # type: ignore
from click import Context, Option, Parameter

from execenv import dotenv
from execenv.config import DEFAULT_CONFIG
from execenv.utils import add_flags_callback, add_help_callback
from execenv.verbose import VerboseInfo


def is_test_mode():
    return bool(os.getenv("EXECENV_TEST", ""))


def _no_traceback_excepthook(
    exctype: Type[BaseException],
    value: BaseException,
    traceback: Optional[TracebackType],
    /,
):
    pass


def completion_callback(
    ctx: Context,
    param: Union[Option, Parameter] = None,  # type: ignore
    value: Any = None,  # type: ignore
):
    if not is_test_mode():
        enable_click_shell_completion(ctx.command.name)


def config_callback(ctx: Context, param: Union[Option, Parameter], value: Path):
    config = DEFAULT_CONFIG.copy()

    # Load config file
    if value.exists():
        try:
            config.update(dotenv.parse(value.read_text()))
        except Exception as e:
            click.secho(f"Warning: Failed to load .execenv.env ({e})", fg="yellow")
            pass
    else:
        value.write_text("\n".join(f"{k}={v}" for k, v in config.items()))

    ctx.default_map = config


def cwd_callback(ctx: Context, param: Union[Option, Parameter], value: str):
    return os.path.abspath(value) if value else None


def env_callback(
    ctx: Context, param: Union[Option, Parameter], values: Tuple[Tuple[str, str]]
):
    env = {}
    for value in values:
        var_name, var_val = value
        env[var_name] = var_val
    return env


def append_to_env(env: Dict[str, str], key: str, value: str, separator: str):
    if key in env:
        env[key] += separator + value
    else:
        env[key] = value


def append_env_callback(
    ctx: Context, param: Union[Option, Parameter], values: Tuple[Tuple[str, str]]
):
    env: Dict[str, str] = {}
    for value in values:
        var_name, var_val = value
        append_to_env(
            env, var_name, var_val, cast(str, ctx.params.get("append_separator"))
        )
    return env


def env_file_callback(
    ctx: Context, param: Union[Option, Parameter], values: Tuple[TextIOWrapper]
):
    env_from_file = {}

    for value in values:
        try:
            env_from_file.update(dotenv.parse(value.read()))
        except Exception:
            raise click.BadParameter(".env file must be valid")

    return env_from_file


def get_shell_env_varref_format(var: str, escaped: bool = False) -> str:
    system = platform.system()
    if system in ("Linux", "Darwin"):  # Darwin is the system name for macOS
        varref_format = f"${var}" if not escaped else f"\\${var}"
    elif system == "Windows":
        varref_format = f"%{var}%" if not escaped else f"%^{var}%"
    else:
        raise NotImplementedError(f"Unsupported platform: {system}")
    return varref_format


def convert_env_varref(prefix: str, value: str) -> str:
    pattern = rf"\b{prefix}([A-Za-z_][A-Za-z0-9_]*)\b"
    return re.sub(pattern, get_shell_env_varref_format(r"\1"), value)


@add_help_callback(completion_callback)
@add_flags_callback("--version", callback=completion_callback)
@click.command(help=metadata(__package__)["Summary"], no_args_is_help=True)
@click.argument("command", type=str, nargs=-1, required=True)
@click.option(
    "--config",
    type=click.Path(dir_okay=False, path_type=Path),  # type: ignore
    default=Path.home() / ".execenv.env",
    callback=config_callback,
    is_eager=True,
    expose_value=False,
    help='.env config file for execenv. "~/.execenv.env" by default.',
)
@click.option(
    "-c",
    "--clear",
    is_flag=True,
    default=False,
    help="Clear the current environment. False by default.",
)
@click.option(
    "-s",
    "--shell",
    is_flag=True,
    default=False,
    help="Use shell to run the command. False by default.",
)
@click.option(
    "--shell-strict",
    is_flag=True,
    default=False,
    help='Use "shlex.join" to get better shell compatibility and security. False by default.',
)
@click.option(
    "--env-varref-prefix",
    type=str,
    help='Prefix for environment variable references. "EXECENV_" by default.',
)
@click.option(
    "-e",
    "--env",
    multiple=True,
    type=(str, str),
    callback=env_callback,
    help='Set environment variable to given value. Should be in the format of "NAME val".',
)
@click.option(
    "-a",
    "--append-env",
    multiple=True,
    type=(str, str),
    callback=append_env_callback,
    help='Append given value to environment variable rather than replacing it. If not present, it will be set. Might be useful for PATH-like variables. Should be in the format of "NAME val".',
)
@click.option(
    "--append-separator",
    type=str,
    help='Separator to use when appending to environment variable. Only valid with "-a" / "--append-env". "os.pathsep" by default, which is platform-dependent.',
)
@click.option(
    "-f",
    "--file",
    multiple=True,
    type=click.File("r"),
    callback=env_file_callback,
    help=".env file with environment variable pairs.",
)
@click.option(
    "-C",
    "--cwd",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    callback=cwd_callback,
    help="Current working directory.",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Run with verbose mode. Log out necessary info.",
)
@click.version_option(
    None, "--version", "-V", prog_name=__name__, message="%(prog)s v%(version)s"
)
@click.help_option("-h", "--help")
@rich_config(help_config)
def execenv(
    command: Tuple[str, ...],
    env: Dict[str, str],
    append_env: Dict[str, str],
    append_separator: str,
    env_varref_prefix: str,
    clear: bool,
    cwd: Optional[str],
    verbose: Optional[int],
    file: Dict[str, str],
    shell: bool,
    shell_strict: bool,
):
    TEST_MODE = is_test_mode()
    if not TEST_MODE:
        enable_click_shell_completion(execenv.name)

    try:
        # Convert env references to platform-dependent format
        command = tuple(map(partial(convert_env_varref, env_varref_prefix), command))

        # Verbose info
        verbose_info = VerboseInfo(locals(), verbose)

        # Construct merged environment
        env_merged: Dict[str, str] = {}
        if not clear:
            env_merged.update(os.environ)
        env_merged.update(file)
        env_merged.update(env)
        for key, value in append_env.items():
            append_to_env(env_merged, key, value, append_separator)
        verbose_info.add("env_merged", env_merged, 2)

        # Actual command running
        command_str: str = (
            subprocess.list2cmdline(command)
            if not shell_strict
            else shlex.join(command)
        )
        verbose_info.add("actual_command", command_str, 1)

        verbose_info.show()

        result = subprocess.run(
            command_str if shell else command,
            env=env_merged,
            cwd=cwd,
            shell=shell,
            capture_output=TEST_MODE,
            text=TEST_MODE,
        )
        if TEST_MODE:
            sys.stdout.write(result.stdout)
            sys.stderr.write(result.stderr)

        exit(result.returncode)

    except KeyboardInterrupt:
        # Prevent default traceback
        if sys.excepthook is sys.__excepthook__:
            sys.excepthook = _no_traceback_excepthook
        raise


def clink_completion(command: click.Command, completions_path: Path):
    flags: List[str] = []
    descriptions: List[str] = []

    for param in command.params:
        if not isinstance(param, Option):
            continue

        opts = tuple(map(lambda opt: f"'{opt}'", param.opts))
        flags += opts
        if param.help:
            for opt in opts:
                descriptions.append(f"[{opt}] = '{param.help}'")

    flags_str = ", ".join(flags)
    description_str = ",\n".join(descriptions)
    description_str_indented = indent(
        description_str,
        " " * 12,
        lambda line: not description_str.startswith(line),
    )

    script = dedent(f"""\
        local matcher = clink.argmatcher('{command.name}')
        matcher:addflags({flags_str})

        local function adddescriptions_helper(matcher, ...)
            if matcher and matcher.adddescriptions then
                matcher:adddescriptions(...)
            end
        end

        adddescriptions_helper(matcher, {{
            {description_str_indented}
        }})
    """)

    file_path = completions_path / f"{command.name}.lua"

    if file_path.exists():
        click.confirm(
            f"File {f'{command.name}.lua'} already exists. Overwrite?",
            abort=True,
            default=False,
            prompt_suffix=" ",
        )
        click.echo()

    with open(file_path, "w") as f:
        f.write(script)

    click.echo(
        f"Completion script saved to {click.style(str(file_path), fg='yellow', bold=True)}."
    )


@add_help_callback(completion_callback)
@add_flags_callback("--version", callback=completion_callback)
@click.command(
    help="Command to manually setup tab completion for execenv.", no_args_is_help=True
)
@click.option(
    "-s",
    "--shell",
    type=click.Choice(["clink"]),
    required=True,
    help="Shell to setup tab completion.",
)
@click.option(
    "-p",
    "--path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),  # type: ignore
    default=Path.cwd(),
    help="Path where the completion script will be saved. Current directory by default.",
)
@click.version_option(
    None, "--version", "-V", prog_name=__name__, message="%(prog)s v%(version)s"
)
@click.help_option("-h", "--help")
@rich_config(help_config)
def execenv_completion(shell: str, path: Path):
    if not is_test_mode():
        enable_click_shell_completion(execenv_completion.name)

    if shell == "clink":
        completions_path = path / "completions"
        if not completions_path.exists():
            click.confirm(
                f"Directory does not exist.\nWill create at {click.style(str(completions_path), fg='yellow', bold=True)}.\nContinue?",
                default=True,
                abort=True,
                prompt_suffix=" ",
            )
            click.echo()
            completions_path.mkdir()

        clink_completion(execenv, completions_path)
        clink_completion(execenv_echo, completions_path)
        clink_completion(execenv_completion, completions_path)

        click.echo("\nRun following to install auto-completion:")
        click.secho(f'\nclink installscripts "{path}"\n', fg="yellow", bold=True)
        click.echo("Restart your shell to load the completion script.")
    else:
        raise click.BadParameter("Shell is not supported.")


@add_help_callback(completion_callback)
@add_flags_callback("--version", callback=completion_callback)
@click.command(
    help="Test command to show value of given environment variables.",
    no_args_is_help=True,
)
@click.argument("env", type=str, nargs=-1, required=True)
@click.version_option(
    None, "--version", "-V", prog_name=__name__, message="%(prog)s v%(version)s"
)
@click.help_option("-h", "--help")
@rich_config(help_config)
def execenv_echo(env: Tuple[str, ...]):
    if not is_test_mode():
        enable_click_shell_completion(execenv_echo.name)

    for e in env:
        click.echo(f"{e}=" + os.getenv(e, click.style("NOT FOUND", fg="red")))


if __name__ == "__main__":
    execenv()
