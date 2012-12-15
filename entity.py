import pygame

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

    def move(self, x, y):
        self.oldx = self.x
        self.oldy = self.y
        self.x = x
        self.y = y

    def hit(self, other):
        pass

    def hit_world(self, world, hitpos):
        pass

    def render(self, surf):
        # Hack to avoid clearing screen every frame
        rect = pygame.Rect(self.oldx, self.oldy, self.w, self.h)
        surf.fill(pygame.Color(0, 0, 0), rect)

class Bullet(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x, y, 40, 10)

    def render(self, surf):
        Entity.render(self, surf)
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(surf, pygame.Color(255, 0, 0), rect)

    def hit_world(self, world, hitpos):
        for i in range(hitpos[0] - 1, hitpos[0] + 1):
            for j in range(hitpos[1] - 1, hitpos[1] + 1):
                if world.hit(i, j):
                    self.removeme = True
