import pygame


class Tile:

    SIZE = 16

    def __init__(self, color):
        self.color = color
        self.destroyed = False

    def render(self, surf, x, y):
        if not self.destroyed:
            rect = pygame.Rect(x, y, Tile.SIZE, Tile.SIZE)
            pygame.draw.rect(surf, self.color, rect)

    def hit(self):
        self.destroyed = True

class World:

    NULLTILE = Tile(pygame.Color(255, 0, 255)) # Obnoxious color
    WATERTILE = Tile(pygame.Color(50, 100, 255))
    GROUNDTILE = Tile(pygame.Color(71, 139, 0))

    def __init__(self, width, height, inittile=GROUNDTILE):
        self.width = width
        self.height = height
        self.tiles = []
        for i in range(width * height):
            self.tiles.append(inittile)

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

    def render(self, surf, x, y):
        for i in range(self.width):
            for j in range(self.height):
                tile = self.get(i, j)
                tile.render(surf, x + i * (Tile.SIZE + 1),
                                  y + j * (Tile.SIZE + 1))
