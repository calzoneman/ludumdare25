#!/usr/bin/env python
import pygame
from pygame.locals import *

import math

from world import Tile, World
from entity import Entity, Bullet, Player
from physics import Physics
from keyboard import Keyboard

pygame.init()
pygame.display.init()

WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE | DOUBLEBUF)

running = True
keyboard = Keyboard()
world = World(32, 32)
off = ((WIDTH - world.get_render_width()) / 2,
       (HEIGHT - world.get_render_height()) / 2)
world.offX = off[0]
world.offY = off[1]
ply = Player(20, 20, world)
physics = Physics(world, (WIDTH, HEIGHT))
physics.watch(ply)
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
            world.regen_once()
        elif ev.type == MOUSEBUTTONDOWN:
            mpos = ev.pos
            center = ply.get_center()
            a = mpos[0] - center[0]
            b = mpos[1] - center[1]
            # tan(ang) = b / a
            ang = math.atan2(b, a)

            # Calculate bullet pos
            pos = [math.cos(ang) * ply.w + center[0],
                   math.sin(ang) * ply.h + center[1]]

            bull = Bullet(pos[0], pos[1], world)
            speed = 2
            bull.vx = speed * math.cos(ang)
            bull.vy = speed * math.sin(ang)
            physics.watch(bull)

        elif ev.type == KEYDOWN:
            keyboard.keydown(ev.key)
        elif ev.type == KEYUP:
            keyboard.keyup(ev.key)

    # Handle movement
    if keyboard.is_down(K_w):
        ply.vy = -1
    elif keyboard.is_down(K_s):
        ply.vy = 1
    else:
        ply.vy = 0
    if keyboard.is_down(K_a):
        ply.vx = -1
    elif keyboard.is_down(K_d):
        ply.vx = 1
    else:
        ply.vx = 0

    if world.win():
        print "You Win!"
    world.render(screen)
    physics.tick()
    physics.render(screen)
    pygame.display.flip()


    dt = pygame.time.get_ticks() - last
    if dt < (1000 / 60):
        pygame.time.delay((1000 / 60) - dt)
    last = pygame.time.get_ticks()
pygame.quit()
