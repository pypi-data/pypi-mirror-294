from enum import auto

import pygame

font = {}

NORMAL = auto()
HEADING = auto()
GREEN = (46, 176, 80)
RED = (163, 48, 42)


def init():
    pygame.font.init()
    font[NORMAL] = pygame.font.SysFont("freesansbold", 36)
    font[HEADING] = pygame.font.SysFont("freesansbold", 72)
    # fonts = pygame.font.get_fonts()
    # pass


def createMessage(msg, style=NORMAL, colour=GREEN):
    textSurface = font[style].render(msg, True, colour)
    return textSurface
