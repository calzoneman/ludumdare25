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
world = World(32, 32, off=(150, 50))
physics = Physics(world)
bullet = Bullet(0, 80)
bullet.vx = 1
physics.watch(bullet)
clock = pygame.time.Clock()
pygame.time.set_timer(USEREVENT, 1000)
last = pygame.time.get_ticks()

while running:
    clock.tick(0)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            running = False
            break
        elif ev.type == USEREVENT:
            print clock.get_fps()
        elif ev.type == MOUSEBUTTONDOWN:
            bull = Bullet(ev.pos[0], ev.pos[1])
            if ev.pos[0] < world.offX:
                bull.vx = 1
            elif ev.pos[0] > world.offX + world.get_render_width():
                bull.vx = -1
            if ev.pos[1] < world.offY:
                bull.vy = 1
            elif ev.pos[1] > world.offY + world.get_render_height():
                bull.vy = -1
            physics.watch(bull)
    world.render(screen)
    physics.tick()
    physics.render(screen)
    pygame.display.flip()

    dt = pygame.time.get_ticks() - last
    if dt < (1000 / 60):
        pygame.time.delay((1000 / 60) - dt)
    last = pygame.time.get_ticks()
pygame.quit()
