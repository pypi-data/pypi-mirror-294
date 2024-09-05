import pygame
from magic_lantern import config
from magic_lantern import log

WIDTH, HEIGHT = (1280, 720)


# Since the configuration isn't initialized yet, we need to explicitly
# initialize here.
def init():
    global displaySurface
    global WIDTH, HEIGHT

    # pygame setup
    pygame.init()
    pygame.mixer.quit()  # Don't need
    pygame.joystick.quit()  # Don't need

    log.debug(f"Support for all image formats: {pygame.image.get_extended()}")
    if config.fullscreen:
        displaySurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))

    WIDTH, HEIGHT = displaySurface.get_size()
    log.info(f"Screen size {WIDTH} x {HEIGHT}")

    pygame.mouse.set_visible(False)


def rect():
    return pygame.Rect(0, 0, WIDTH, HEIGHT)
