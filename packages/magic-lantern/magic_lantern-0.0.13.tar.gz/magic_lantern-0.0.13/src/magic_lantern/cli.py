import sys
import click
import pathlib

from magic_lantern import log, config, controller, snafu


@click.command(
    epilog="""To reload the configuration, send it the USR1 signal:

    pkill -USR1 magic-lantern
\b    

See https://github.com/normanlorrain/magic-lantern for more details."""
)
@click.version_option()
@click.option(
    "-c",
    "--config-file",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
    help="Configuration file.",
)
@click.option(
    "-f", "--fullscreen", is_flag=True, show_default=True, help="Full screen mode"
)
@click.option(
    "-s", "--shuffle", is_flag=True, show_default=True, help="Shuffle the slides"
)
@click.option(
    "-i",
    "--interval",
    type=click.IntRange(min=1, max=None),
    required=False,
    help="Interval (seconds) between images.",
)
@click.argument(
    "directory",
    type=click.Path(
        exists=True, resolve_path=True, dir_okay=True, path_type=pathlib.Path
    ),
    required=False,
)
def magic_lantern(config_file, fullscreen, shuffle, interval, directory):
    """A slide show generator. Specify a directory containing image files or use -c to specify a config file."""

    # At this point switches --version and --help have been dealt with by click.
    # Therefore we can initialize our log (which we start with an enpty file)
    log.init()

    if config_file == None and directory == None:
        raise click.ClickException("Must specify a DIRECTORY or a config file.")
    if config_file and directory:
        log.warning(
            "Warning: -c and DIRECTORY are mutually exclusive. DIRECTORY will be ignored"
        )
    if directory:
        log.info(f"Single directory slide show: {directory}")

    runState = True
    while runState:
        config.init(config_file, fullscreen, shuffle, interval, directory)
        controller.init()
        runState = controller.run()


def cli():
    try:
        magic_lantern()
    except SystemExit:
        log.info("Application ended normally (System Exit)")
    except KeyboardInterrupt:
        log.warning("Application ended (KeyboardInterrupt)")
    except snafu.Snafu as e:
        log.error(e)
    except Exception as e:
        log.exception(
            "Application ended. (UNCAUGHT EXCEPTION)",
        )
