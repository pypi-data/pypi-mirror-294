import pathlib

import pygame
import exifread

from magic_lantern import screen, log, config

_slideCache: dict = {}

EXIF_DATE = "EXIF DateTimeOriginal"
EXIF_ORIENTATION = "Image Orientation"


def clearCache():
    _slideCache.clear()


def createSlide(path: str, interval: int):
    if path in _slideCache:
        slide = _slideCache[path]
    else:
        slide = Slide(path, interval)
        _slideCache[path] = slide
    log.info(f"{slide.path.name}")
    return


def getSlide(path: str):
    return _slideCache[path]


class SlideException(Exception):
    def __init__(self, filename):
        self.filename = filename


class Slide:
    def __init__(self, filename, interval) -> None:
        self.filename = filename
        self.path = pathlib.Path(self.filename)
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.datetime = ""
        self.exif_orientation = None
        self.interval = interval
        self.imageLoaded = False

    def loadImage(self):
        log.debug(f"{self.path.name}")

        # Load the image
        try:
            image = pygame.image.load(self.filename)
        except:
            raise SlideException(self.filename)
        self.width = image.get_width()
        self.height = image.get_height()
        # Read Exif tags
        tags = exifread.process_file(open(self.filename, "rb"), details=False)

        if EXIF_DATE in tags:
            self.datetime = tags[EXIF_DATE]
        if EXIF_ORIENTATION in tags:
            self.exif_orientation = tags[EXIF_ORIENTATION]
            log.debug(self.exif_orientation)
            if 3 in self.exif_orientation.values:
                image = pygame.transform.rotate(image, 180)
            elif 6 in self.exif_orientation.values:
                image = pygame.transform.rotate(image, 270)
            elif 8 in self.exif_orientation.values:
                image = pygame.transform.rotate(image, 90)

        # Get the boundary rectangle
        imageRect = pygame.Rect((0, 0), image.get_size())

        # Fit the rectangle to the screen
        imageFit = imageRect.fit(screen.rect())

        self.x = imageFit.x
        self.y = imageFit.y

        # Scale the image to the rectangle
        scaledImage = pygame.transform.smoothscale(
            image.convert(), imageFit.size
        )  # call convert to upscale any 8-bit images

        self.surface = scaledImage.convert()

        self.imageLoaded = True

    def coordinates(self):
        if not self.imageLoaded:
            self.loadImage()
        log.debug(f"Coordinates x,y: {self.x},{self.y}")
        return (self.x, self.y)

    def getSurface(self):
        if not self.imageLoaded:
            self.loadImage()
        log.info(f"{self.path.name} ({self.width} x {self.height})")
        return self.surface
