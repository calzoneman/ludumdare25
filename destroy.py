#!/usr/bin/env python
import pygame
from pygame.locals import *

from world import Tile, World

pygame.init()
pygame.display.init()

WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE | DOUBLEBUF)

running = True
world = World(16, 16)

while running:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            running = False
            break

    world.render(screen, 50, 50)
    pygame.display.flip()


pygame.quit()
