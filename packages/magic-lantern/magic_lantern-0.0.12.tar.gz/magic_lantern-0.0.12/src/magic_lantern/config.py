import pathlib
import os
import enum
import tomllib
import sys

from magic_lantern import log

this_mod = sys.modules[__name__]

configRoot: pathlib.Path = None
fullscreen: bool = False
interval: int = 5

EXCLUDE = "exclude"
FULLSCREEN = "fullscreen"
ALBUMS = "albums"
ORDER = "order"
FOLDER = "folder"
WEIGHT = "weight"
INTERVAL = "interval"


class Order(enum.StrEnum):
    SEQUENCE = "sequence"
    ATOMIC = "atomic"
    RANDOM = "random"


def init(
    configFile: pathlib.Path | None,
    fullscreen_: bool,
    shuffle: bool,
    interval_: int,
    path: pathlib.Path,
):

    # This is the folder that the slides are found in
    global configRoot
    if configFile:
        configRoot = configFile.parent
        _dictConfig = loadConfig(configFile)
    else:  # create a simple album
        configRoot = os.getcwd()
        _dictConfig = createConfig(path, shuffle)

    # Validate the albums. Make a copy first, then loop
    # and update with validated fields
    albumList = list(_dictConfig[ALBUMS])
    _dictConfig[ALBUMS].clear()
    for album in albumList:
        try:
            validateAlbumPath(album)
            validateAlbumOrder(album)
            validateAlbumParams(album)
            _dictConfig[ALBUMS].append(album)
        except ValidationError as e:
            log.error(e)

    for i in _dictConfig:
        setattr(this_mod, i, _dictConfig[i])
    pass

    # If the config file doesn't specify a weight, set it here.
    # Each album can set it's own weight which will override this.
    if not hasattr(this_mod, WEIGHT):
        setattr(this_mod, WEIGHT, 1)

    # If the config file doesn't specify exclude, set it here.
    if not hasattr(this_mod, EXCLUDE):
        setattr(this_mod, EXCLUDE, [])

    # If the config file doesn't specify an interval, set it here.
    # Each album can set it's own interval which will override this.
    if not hasattr(this_mod, INTERVAL):
        setattr(this_mod, INTERVAL, 1)

    # This is passed from the command line, and thus overrides any setting that
    # came from the config file above.
    if interval_:
        global interval
        interval = interval_

    # This is passed from the command line, and thus overrides any setting that
    # came from the config file above.
    if fullscreen_:
        global fullscreen
        fullscreen = fullscreen_


def loadConfig(configFile):
    with open(configFile, "rb") as fp:
        return tomllib.load(fp)


def createConfig(path, shuffle):

    return {
        ALBUMS: [{ORDER: "random" if shuffle else "sequence", FOLDER: path, WEIGHT: 1}]
    }


class ValidationError(Exception):
    pass


def validateAlbumParams(album):
    for key in [WEIGHT, INTERVAL]:
        if key in album:
            if type(album[key]) != int:
                raise ValidationError(
                    "Configuration: bad value for {key} in album {path}"
                )


def validateAlbumOrder(album):
    if ORDER in album:
        if album[ORDER] not in [e.value for e in Order]:
            raise ValidationError(
                "Configuration: bad value for {ORDER} in album {path}"
            )


def validateAlbumPath(album: dict):
    path = pathlib.Path(album[FOLDER])
    if not path.is_absolute():
        path = configRoot / path

    if path.exists():
        album[FOLDER] = path
    else:
        raise ValidationError(f"Configuration: invalid path: {path}")
