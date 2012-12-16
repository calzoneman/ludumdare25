import pygame
import math
import random


def sign(x):
    if x == 0:
        return 0
    else:
        return x / math.fabs(x)

class Entity:
    def __init__(self, x, y, w, h, world):
        self.x = x
        self.y = y
        self.oldx = x
        self.oldy = y
        self.w = w
        self.h = h
        self.world = world
        self.vx = 0
        self.vy = 0
        self.health = 0
        self.removeme = False

    def takedamage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.die()

    def think(self):
        pass

    def die(self):
        self.removeme = True

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

    def hit_world(self, hits):
        pass

    def hit_edge(self, screensize):
        pass

    def render(self, surf):
        pass

    def clear(self, surf):
        # Hack to avoid clearing screen every frame
        rect = pygame.Rect(self.oldx, self.oldy, self.w, self.h)
        surf.fill(pygame.Color(0, 0, 0), rect)
        # Find hit positions at old position, redraw them
        x = self.x
        y = self.y
        self.x = self.oldx
        self.y = self.oldy
        hits = self.world.entity_hitpos(self)
        if hits:
            for hitpos in hits:
                for i in range(hitpos[0] - 1, hitpos[0] + 1):
                    for j in range(hitpos[1] - 1, hitpos[1] + 1):
                        self.world.get(i, j).needsRedraw = True
        # Restore position
        self.x = x
        self.y = y

class Bullet(Entity):
    # To make things easier, bullets can just be square :)
    SIZE = 10
    DAMAGE = 1
    def __init__(self, x, y, world):
        Entity.__init__(self, x, y, Bullet.SIZE, Bullet.SIZE, world)

    def render(self, surf):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(surf, pygame.Color(255, 0, 0), rect)

    def hit(self, other):
        if not isinstance(other, Enemy):
            return
        other.takedamage(Bullet.DAMAGE)
        self.removeme = True

    def hit_world(self, hits):
        for hitpos in hits:
            for i in range(hitpos[0] - 1, hitpos[0] + 1):
                for j in range(hitpos[1] - 1, hitpos[1] + 1):
                    if self.world.hit(i, j):
                        self.removeme = True
                    self.world.get(i, j).needsRedraw = True

    def hit_edge(self, screensize):
        self.removeme = True

class Player(Entity):
    def __init__(self, x, y, world):
        Entity.__init__(self, x, y, 32, 32, world)
        self.health = 20
        self.lives = 3

    def render(self, surf):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        surf.fill(pygame.Color(0, 255, 255), rect)

    def die(self):
        self.lives -= 1
        self.health = 20
        self.removeme = True

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


    def hit_world(self, hits):
        collide = False
        for hitpos in hits:
            if not self.world.get(hitpos[0], hitpos[1]).destroyed:
                collide = True

        if collide:
            x = 0.1 * sign(self.vx)
            y = 0.1 * sign(self.vy)
            while collide:
                collide = False
                self.x = self.x - x
                self.y = self.y - y

                hits = self.world.entity_hitpos(self)
                if not hits:
                    break
                for pos in hits:
                    if not self.world.get(pos[0], pos[1]).destroyed:
                        collide = True

    def hit_edge(self, screensize):
        x = 0.1 * sign(self.vx)
        y = 0.1 * sign(self.vy)
        at_edge = True
        while at_edge:
            at_edge = False
            self.x = self.x - x
            self.y = self.y - y
            at_edge = self.x < 0 or self.y < 0
            at_edge = at_edge or self.x + self.w >= screensize[0]
            at_edge = at_edge or self.y + self.h >= screensize[1]

class EnemyBullet(Entity):
    # To make things easier, bullets can just be square :)
    SIZE = 5
    DAMAGE = 1
    def __init__(self, x, y, world):
        Entity.__init__(self, x, y, EnemyBullet.SIZE, EnemyBullet.SIZE, world)

    def render(self, surf):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(surf, pygame.Color(255, 0, 0), rect)

    def hit(self, other):
        if not isinstance(other, Player):
            return
        other.takedamage(EnemyBullet.DAMAGE)
        self.removeme = True

    def hit_edge(self, screensize):
        self.removeme = True

class Enemy(Entity):
    SPEED = 0.6
    def __init__(self, x, y, world, physics):
        Entity.__init__(self, x, y, 16, 16, world)
        self.health = 5
        self.physics = physics
        self.ticks = 0

    def hit(self, other):
        if isinstance(other, Player):
            other.takedamage(5)
            self.takedamage(5)

    def think(self, ply):
        center = self.get_center()
        dy = ply.y - center[1]
        dx = ply.x - center[0]
        ang = math.atan2(dy, dx)

        self.vx = Enemy.SPEED * math.cos(ang)
        self.vy = Enemy.SPEED * math.sin(ang)

        if self.ticks % 60 == 0:
            pos = [math.cos(ang) * self.w + center[0],
                   math.sin(ang) * self.h + center[1]]
            bullet = EnemyBullet(pos[0], pos[1], self.world)
            speed = 2
            bullet.vx = speed * math.cos(ang)
            bullet.vy = speed * math.sin(ang)
            self.physics.watch(bullet)

        self.ticks += 1

    def render(self, surf):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        surf.fill(pygame.Color(255, 255, 0), rect)

class Particle(Entity):

    COLORS = [pygame.Color(255, 187, 0),
              pygame.Color(255, 0, 0),
              pygame.Color(255, 255, 0),
              pygame.Color(187, 187, 187)]

    def __init__(self, x, y, size, world, color=None):
        Entity.__init__(self, x, y, size, size, world)
        if color is None:
            color = random.choice(Particle.COLORS)
        self.color = color
        self.ticks = 0
        self.lifetime = random.randint(40, 100)
        ang = random.random() * 2 * 3.14
        self.vx = (random.random() * 0.8) * math.cos(ang)
        self.vy = (random.random() * 0.8) * math.sin(ang)

    def render(self, surf):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(surf, self.color, rect)

    def think(self):
        if self.ticks == self.lifetime:
            self.removeme = True

        if self.vx < 0:
            self.vx += 0.01
        if self.vx > 0:
            self.vx -= 0.01
        if math.fabs(self.vx) < 0.01:
            self.vx = 0
        if self.vy < 0:
            self.vy += 0.01
        if self.vy > 0:
            self.vy -= 0.01
        if math.fabs(self.vy) < 0.01:
            self.vy = 0

        self.ticks += 1

    def hit_edge(self, screensize):
        self.removeme = True
