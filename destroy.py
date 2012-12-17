#!/usr/bin/env python
import pygame
from pygame.locals import *

import math
import random
import sys

from world import Tile, World
from entity import Entity, Bullet, Player, Enemy
from physics import Physics
from keyboard import Keyboard

pygame.init()
pygame.display.init()
pygame.display.set_caption("Earthmageddon")
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

WIDTH = 800
HEIGHT = 600

flags = HWSURFACE | DOUBLEBUF | SRCALPHA
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)

# Event definitions
FRAMECOUNTER = USEREVENT
WORLDREGEN   = USEREVENT+1
ENTITYGEN    = USEREVENT+2

pygame.time.set_timer(FRAMECOUNTER, 1000)
pygame.time.set_timer(WORLDREGEN, 3000)
pygame.time.set_timer(ENTITYGEN, 5000)

# Font init
bigfont = pygame.font.Font(None, 40)
hugefont = pygame.font.Font(None, 100)
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)

# Sound init
shootsound = pygame.mixer.Sound("shoot.wav")

def title():
    start = False
    cyan = pygame.Color(0, 255, 255)
    while not start:
        for ev in pygame.event.get():
            if ev.type == KEYDOWN:
                if ev.key == K_SPACE:
                    start = True
                    break
            elif ev.type == QUIT:
                pygame.quit()
                sys.exit(0)

        title = hugefont.render("Earthmageddon", 1, cyan, black)
        x = (WIDTH - title.get_width()) / 2
        y = 100
        screen.blit(title, (x, y))
        y += title.get_height() + 10

        text = bigfont.render("by calzoneman", 1, cyan, black)
        x = (WIDTH - text.get_width()) / 2
        screen.blit(text, (x, y))
        y += text.get_height() + 20

        text = bigfont.render("WASD to move, click to fire", 1, white, black)
        x = (WIDTH - text.get_width()) / 2
        screen.blit(text, (x, y))
        y += text.get_height() + 10

        text = bigfont.render("Destroy the world (it regenerates)", 1, white, black)
        x = (WIDTH - text.get_width()) / 2
        screen.blit(text, (x, y))
        y += text.get_height() + 10

        text = bigfont.render("Avoid enemy fire, shoot them down!", 1, white, black)
        x = (WIDTH - text.get_width()) / 2
        screen.blit(text, (x, y))
        y += text.get_height() + 50


        space = bigfont.render("Press space to begin", 1, white, black)
        x = (WIDTH - space.get_width()) / 2
        screen.blit(space, (x, y))

        pygame.display.flip()


def game():
    screen.fill(black)
    running = True
    keyboard = Keyboard()
    world = World(32, 32)
    off = ((WIDTH - world.get_render_width()) / 2,
           (HEIGHT - world.get_render_height()) / 2)
    world.offX = off[0]
    world.offY = off[1]
    ply = Player(0, 0, world)
    ply.x = random.randint(0, WIDTH - ply.w)
    ply.y = random.randint(0, HEIGHT - ply.h)
    while world.entity_hitpos(ply):
        ply.x = random.randint(0, WIDTH - ply.w)
        ply.y = random.randint(0, HEIGHT - ply.h)
    physics = Physics(world, (WIDTH, HEIGHT))
    physics.watch(ply)
    clock = pygame.time.Clock()
    last = pygame.time.get_ticks()
    ticks = 0
    plydeathtimer = 0
    lastrect = pygame.Rect(0, 0, 0, 0)

    while running:
        ticks += 1
        clock.tick(0)
        for ev in pygame.event.get():
            if ev.type == QUIT:
                running = False
                break
            elif ev.type == FRAMECOUNTER:
                print clock.get_fps()
            elif ev.type == WORLDREGEN:
                world.regen_once()
            elif ev.type == ENTITYGEN:
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                physics.watch(Enemy(x, y, world, physics))
            elif ev.type == MOUSEBUTTONDOWN:
                if ev.button == 0 and plydeathtimer == 0:
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
                    shootsound.play()

            elif ev.type == KEYDOWN:
                keyboard.keydown(ev.key)
            elif ev.type == KEYUP:
                keyboard.keyup(ev.key)

        # Handle movement
        if plydeathtimer == 0:
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

        # Shooting repeat
        if ticks % 10 == 0 and pygame.mouse.get_pressed()[0]:
            mpos = pygame.mouse.get_pos()
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
            shootsound.play()


        for ent in physics.entities:
            if isinstance(ent, Enemy):
                ent.think(ply)

        if world.win():
            win()
            running = False
        if ply.lives == 0:
            lose()
            running = False
        elif ply.removeme:
            ply.removeme = False
            plydeathtimer = 180
        if plydeathtimer > 0:
            if plydeathtimer == 1:
                ply.x = random.randint(0, WIDTH - ply.w)
                ply.y = random.randint(0, HEIGHT - ply.h)
                while world.entity_hitpos(ply):
                    ply.x = random.randint(0, WIDTH - ply.w)
                    ply.y = random.randint(0, HEIGHT - ply.h)
                physics.watch(ply)
            plydeathtimer -= 1

        # Clear previous font
        screen.fill(black, lastrect)

        # Render
        physics.renderclear(screen)
        world.render(screen)
        physics.tick()
        physics.render(screen)

        # Display health
        msg = "Lives: %d | Health: %d" % (ply.lives, ply.health)
        text = bigfont.render(msg, 1, white)
        lastrect = pygame.Rect(0, 0, text.get_width(), text.get_height())
        screen.blit(text, (0, 0))
        pygame.display.flip()


        dt = pygame.time.get_ticks() - last
        if dt < (1000 / 60):
            pygame.time.delay((1000 / 60) - dt)
        last = pygame.time.get_ticks()

def lose():
    exit = False
    red = pygame.Color(187, 0, 0)
    while not exit:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                exit = True
                break
            elif ev.type == KEYDOWN and ev.key == K_SPACE:
                game()
                exit = True
                break

        screen.fill(black)
        text = hugefont.render("YOU LOSE", 1, red, black)
        x = (WIDTH - text.get_width()) / 2
        y = (HEIGHT - text.get_height()) / 2
        screen.blit(text, (x, y))
        y += text.get_height() + 10

        text = bigfont.render("The world is safe once again :(", 1, red, black)
        x = (WIDTH - text.get_width()) / 2
        screen.blit(text, (x, y))
        y += text.get_height() + 50

        text = bigfont.render("Press space to try again", 1, white, black)
        x = (WIDTH - text.get_width()) / 2
        screen.blit(text, (x, y))
        pygame.display.flip()

def win():
    exit = False
    green = pygame.Color(0, 187, 0)
    while not exit:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                exit = True
                break
            elif ev.type == KEYDOWN and ev.key == K_SPACE:
                game()
                exit = True
                break

        screen.fill(black)
        text = hugefont.render("YOU WIN", 1, green, black)
        x = (WIDTH - text.get_width()) / 2
        y = (HEIGHT - text.get_height()) / 2
        screen.blit(text, (x, y))
        y += text.get_height() + 10

        msg = "With Earth destroyed, the universe is yours"
        text = bigfont.render(msg, 1, green, black)
        x = (WIDTH - text.get_width()) / 2
        screen.blit(text, (x, y))
        y += text.get_height() + 50

        text = bigfont.render("Press space to try again", 1, white, black)
        x = (WIDTH - text.get_width()) / 2
        screen.blit(text, (x, y))
        pygame.display.flip()


title()
game()
pygame.quit()
