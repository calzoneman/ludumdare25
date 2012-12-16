from entity import Entity, Enemy, Particle, Player
import random

class Physics:
    def __init__(self, world, size=(640, 480)):
        self.world = world
        self.entities = []
        self.cleared = []
        self.size = size

    def tick(self):
        for ent in self.entities:
            # Enemy.think() needs to accept a Player as an argument
            if not isinstance(ent, Enemy):
                ent.think()
            ent.move(ent.x + ent.vx, ent.y + ent.vy)
            self.entity_collision(ent)

            if not ent.removeme:
                hits = self.world.entity_hitpos(ent)
                if hits:
                    ent.hit_world(hits)

            if not ent.removeme:
                offscreen = ent.x < 0 or ent.y < 0
                offscreen = offscreen or ent.x + ent.w >= self.size[0]
                offscreen = offscreen or ent.y + ent.h >= self.size[1]
                if offscreen:
                    ent.hit_edge(self.size)

            if ent.removeme:
                if isinstance(ent, Enemy) or isinstance(ent, Player):
                    for i in range(random.randint(4, 12)):
                        size = random.randint(3, 6)
                        self.watch(Particle(ent.x, ent.y, size, self.world))
                self.destroy(ent)

    def entity_collision(self, ent):
        for other in self.entities:
            if other != ent and ent.collides(other):
                other.hit(ent)

    def watch(self, entity):
        self.entities.append(entity)

    def destroy(self, entity):
        self.cleared.append(entity)
        self.entities.remove(entity)

    def render(self, surf):
        for ent in self.entities:
            ent.clear(surf)
        for ent in self.cleared:
            ent.clear(surf)
        for ent in self.entities:
            ent.render(surf)
        self.cleared = []
