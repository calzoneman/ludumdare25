import pygame


class Tile:

    SIZE = 16

    def __init__(self, color):
        self.color = color
        self.destroyed = False

    def render(self, surf, x, y):
        rect = pygame.Rect(x, y, Tile.SIZE, Tile.SIZE)
        if self.destroyed:
            pygame.draw.rect(surf, pygame.Color(10, 10, 10), rect)
        else:
            pygame.draw.rect(surf, self.color, rect)

    def hit(self):
        self.destroyed = True

class World:

    NULLTILE = pygame.Color(255, 0, 255) # Obnoxious color
    WATERTILE = pygame.Color(50, 100, 255)
    GROUNDTILE = pygame.Color(71, 139, 0)

    def __init__(self, width, height, inittile=GROUNDTILE, off=(0, 0)):
        self.width = width
        self.height = height
        self.offX = off[0]
        self.offY = off[1]
        self.tiles = []
        for i in range(width * height):
            self.tiles.append(Tile(inittile))

    def in_range(self, x, y):
        return x >= 0 and y >= 0 and x < self.width and y < self.height

    def get(self, x, y):
        if not self.in_range(x, y):
            return World.NULLTILE
        else:
            return self.tiles[y * self.width + x]

    def hit(self, x, y):
        if not self.in_range(x, y):
            return False
        else:
            self.tiles[y * self.width + x].hit()
            return True

    def render(self, surf):
        for i in range(self.width):
            for j in range(self.height):
                tile = self.get(i, j)
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

        xmin = xmin / (Tile.SIZE + 1)
        xmax = xmax / (Tile.SIZE + 1)
        ymin = ymin / (Tile.SIZE + 1)
        ymax = ymax / (Tile.SIZE + 1)

        hit = False
        for xcur in range(xmin, xmax + 1):
            for ycur in range(ymin, ymax + 1):
                hit = self.in_range(xcur, ycur) or hit
                if hit:
                    return (xcur, ycur)

        return hit
