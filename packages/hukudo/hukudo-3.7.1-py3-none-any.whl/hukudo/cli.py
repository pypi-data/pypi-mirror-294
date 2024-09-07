import logging
import os
from pathlib import Path

import click
import structlog
from click import ClickException

import hukudo
from hukudo.exc import HukudoException
from hukudo.log import LOG_LEVELS, configure_structlog_dev
from .gitlab.cli import gitlab
from .grafana.cli import grafana
from .pypi.cli import pypi


@click.group()
@click.option(
    '-l',
    '--log-level',
    type=click.Choice(LOG_LEVELS, case_sensitive=False),
    default=lambda: os.environ.get('LOGLEVEL', 'WARNING'),
)
def root(log_level):
    """
    For completion, add this to ~/.bashrc:

        eval "$(_HUKUDO_COMPLETE=bash_source hukudo)"

    See also https://click.palletsprojects.com/en/8.1.x/shell-completion/
    """
    configure_structlog_dev(log_level)
    logging.basicConfig(format='%(msg)s')
    structlog.getLogger().debug('logging configured', level=log_level)


# noinspection PyTypeChecker
root.add_command(grafana)
# noinspection PyTypeChecker
root.add_command(gitlab)
# noinspection PyTypeChecker
root.add_command(pypi)


@root.command()
def version():
    print(hukudo.__version__)


@root.group()
def chromedriver():
    pass


@chromedriver.command()
@click.option('-s', '--skip-symlink', is_flag=True)
@click.option('-f', '--force', is_flag=True)
@click.argument('target_dir', type=click.Path(path_type=Path), required=False)
def download(skip_symlink, force, target_dir):
    """
    Downloads the latest chromedriver matching your Chrome browser version
    and creates a symlink to it.

    Example:

        hukudo chromedriver download /tmp/

    Results in `/tmp/chromedriver` pointing to `/tmp/chromedriver-101.0.4951.41`.
    """
    import hukudo.chromedriver

    try:
        hukudo.chromedriver.download_and_symlink(
            target_dir, force=force, skip_symlink=skip_symlink
        )
    except HukudoException as e:
        raise ClickException(str(e))


@root.command(name='keepn')
@click.argument('num', type=int)
@click.argument('directory', type=click.Path(path_type=Path))
def keepn_(num: int, directory: Path):
    """Keep NUM files in DIRECTORY and delete the rest."""
    import hukudo.filesystem

    hukudo.filesystem.keepn(directory=directory, n_keep=num)


def main():
    root()


if __name__ == '__main__':
    main()
