import pygame
import math


def sign(x):
    if x == 0:
        return 0
    else:
        return x / math.fabs(x)

class Entity:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.oldx = x
        self.oldy = y
        self.w = w
        self.h = h
        self.vx = 0
        self.vy = 0
        self.health = 0
        self.removeme = False

    def collides(self, other):
        return not (self.x + self.w < other.x or
                    self.y + self.h < other.y or
                    self.x > other.x + other.w or
                    self.y > other.y + other.h)

    def get_center(self):
        return (self.x + self.w / 2, self.y + self.h / 2)

    def move(self, x, y):
        self.oldx = self.x
        self.oldy = self.y
        self.x = x
        self.y = y

    def hit(self, other):
        pass

    def hit_world(self, world, hits):
        pass

    def render(self, surf):
        pass

    def clear(self, surf):
        # Hack to avoid clearing screen every frame
        rect = pygame.Rect(self.oldx, self.oldy, self.w, self.h)
        surf.fill(pygame.Color(0, 0, 0), rect)

class Bullet(Entity):
    # To make things easier, bullets can just be square :)
    SIZE = 10
    def __init__(self, x, y):
        Entity.__init__(self, x, y, Bullet.SIZE, Bullet.SIZE)

    def render(self, surf):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(surf, pygame.Color(255, 0, 0), rect)

    def hit_world(self, world, hits):
        for hitpos in hits:
            for i in range(hitpos[0] - 1, hitpos[0] + 1):
                for j in range(hitpos[1] - 1, hitpos[1] + 1):
                    if world.hit(i, j):
                        self.removeme = True

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x, y, 32, 32)

    def render(self, surf):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        surf.fill(pygame.Color(0, 255, 255), rect)

    def decel(self):
      #  if self.vx < 0:
      #      self.vx += 0.1
      #  if self.vx > 0:
      #      self.vx -= 0.1
      #  if self.vy < 0:
      #      self.vy += 0.1
      #  if self.vy > 0:
      #      self.vy -= 0.1
      self.vx = self.vy = 0

    def accelerate(self, movedir):
      #  self.vx += movedir[0]
      #  if self.vx < -2:
      #      self.vx = -2
      #  if self.vx > 2:
      #      self.vx = 2
      #  self.vy += movedir[1]
      #  if self.vy < -2:
      #      self.vy = -2
      #  if self.vy > 2:
      #      self.vy = 2
      self.vx = movedir[0]
      self.vy = movedir[1]


    def hit_world(self, world, hits):
        collide = False
        for hitpos in hits:
            if not world.get(hitpos[0], hitpos[1]).destroyed:
                collide = True

        if collide:
            x = 0.1 * sign(self.vx)
            y = 0.1 * sign(self.vy)
            while collide:
                collide = False
                self.x = self.x - x
                self.y = self.y - y

                hits = world.entity_hitpos(self)
                if not hits:
                    break
                for pos in hits:
                    if not world.get(pos[0], pos[1]).destroyed:
                        collide = True
