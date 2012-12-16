import pygame
import random
import math


class Tile:

    SIZE = 8

    def __init__(self, color):
        self.color = color
        self.destroyed = False
        self.needsRedraw = True

    def render(self, surf, x, y):
        rect = pygame.Rect(x, y, Tile.SIZE, Tile.SIZE)
        if self.destroyed:
            surf.fill(pygame.Color(40, 40, 40), rect)
        else:
            surf.fill(self.color, rect)
        self.needsRedraw = False

    def hit(self):
        self.destroyed = True
        self.needsRedraw = True

class World:

    NULLTILE = pygame.Color(255, 0, 255) # Obnoxious color
    WATERTILE = pygame.Color(50, 100, 255)
    GROUNDTILE = pygame.Color(71, 139, 0)

    def __init__(self, width, height, off=(0, 0)):
        self.width = width if width > 10 else 10
        self.height = height if height > 10 else 10
        self.offX = off[0]
        self.offY = off[1]
        self.tiles = []
        self.livecount = self.width * self.height
        self.rand = random.Random()
        for i in range(self.width * self.height):
            self.tiles.append(Tile(World.WATERTILE))

        for i in range(self.rand.randint(6, 12)):
            size = self.rand.randint(15, 30)
            x = self.rand.randint(10, self.width-10)
            y = self.rand.randint(10, self.height-10)
            self.create_landmass(x, y, size)

    def create_landmass(self, x, y, size):
        if not self.in_range(x, y) or size < 0:
            return

        self.tiles[y * self.width + x] = Tile(World.GROUNDTILE)

        if not self.rand.randint(0, 2):
            self.create_landmass(x-1, y, size-1)
        if not self.rand.randint(0, 2):
            self.create_landmass(x+1, y, size-1)
        if not self.rand.randint(0, 2):
            self.create_landmass(x, y-1, size-1)
        if not self.rand.randint(0, 2):
            self.create_landmass(x, y+1, size-1)

    def win(self):
        return self.livecount <= 0

    def get_render_width(self):
        return self.width * (Tile.SIZE + 1)

    def get_render_height(self):
        return self.height * (Tile.SIZE + 1)

    def in_range(self, x, y):
        return x >= 0 and y >= 0 and x < self.width and y < self.height

    def regen_once(self):
        x = [0, 0]
        y = [0, 0]
        if self.width % 2 == 0:
            x[0] = int(math.floor(self.width / 2))
            x[1] = x[0] + 1
        else:
            x[0] = x[1] = int(math.floor(self.width / 2))

        if self.height % 2 == 0:
            y[0] = int(math.floor(self.height / 2))
            y[1] = y[0] + 1
        else:
            y[0] = y[1] = int(math.floor(self.height / 2))

        count = 0
        while count == 0 and x[0] >= 0 and y[0] >= 0:
            for i in range(x[0], x[1] + 1):
                for j in range(y[0], y[1] + 1):
                    tile = self.get(i, j)
                    if tile.destroyed:
                        tile.destroyed = False
                        tile.needsRedraw = True
                        count += 1
            x[0] -= 1
            x[1] += 1
            y[0] -= 1
            y[1] += 1
        self.livecount += count

    def get(self, x, y):
        if not self.in_range(x, y):
            return Tile(World.NULLTILE)
        else:
            return self.tiles[y * self.width + x]

    def hit(self, x, y):
        if not self.in_range(x, y):
            return False
        else:
            if not self.tiles[y * self.width + x].destroyed:
                self.livecount -= 1
            self.tiles[y * self.width + x].hit()
            return True

    def render(self, surf):
        for i in range(self.width):
            for j in range(self.height):
                tile = self.get(i, j)
                if tile.needsRedraw:
                    tile.render(surf, self.offX + i * (Tile.SIZE + 1),
                                      self.offY + j * (Tile.SIZE + 1))

    def entity_hit(self, ent):
        xmin = ent.x - self.offX
        ymin = ent.y - self.offY
        xmax = xmin + ent.w
        ymax = ymin + ent.h

        xmin = xmin / (Tile.SIZE + 1)
        xmax = xmax / (Tile.SIZE + 1)
        ymin = ymin / (Tile.SIZE + 1)
        ymax = ymax / (Tile.SIZE + 1)

        hit = False
        for xcur in range(xmin, xmax + 1):
            for ycur in range(ymin, ymax + 1):
                hit = self.hit(xcur, ycur) or hit

        return hit

    def entity_hitpos(self, ent):
        xmin = ent.x - self.offX
        ymin = ent.y - self.offY
        xmax = xmin + ent.w
        ymax = ymin + ent.h

        xmin = int(math.floor(xmin / (Tile.SIZE + 1)))
        xmax = int(math.floor(xmax / (Tile.SIZE + 1)))
        ymin = int(math.floor(ymin / (Tile.SIZE + 1)))
        ymax = int(math.floor(ymax / (Tile.SIZE + 1)))

        hits = []
        for xcur in range(xmin, xmax + 1):
            for ycur in range(ymin, ymax + 1):
                if self.in_range(xcur, ycur):
                    if not self.get(xcur, ycur).destroyed:
                        hits.append((xcur, ycur))
                    self.get(xcur, ycur).needsRedraw = True

        if len(hits) > 0:
            return hits
        else:
            return False
