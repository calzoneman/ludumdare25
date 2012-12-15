#!/usr/bin/env python
import pygame
from pygame.locals import *

from world import Tile, World
from entity import Entity, Bullet
from physics import Physics

pygame.init()
pygame.display.init()

WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE | DOUBLEBUF)

running = True
world = World(16, 16, off=(150, 50))
physics = Physics(world)
bullet = Bullet(0, 80)
bullet.vx = 1
physics.watch(bullet)

while running:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            running = False
            break
    screen.fill(pygame.Color(0, 0, 0))
    world.render(screen)
    physics.tick()
    physics.render(screen)
    pygame.display.flip()
pygame.quit()
