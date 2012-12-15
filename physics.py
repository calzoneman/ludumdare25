from entity import Entity

class Physics:
    def __init__(self, world):
        self.world = world
        self.entities = []

    def tick(self):
        for ent in self.entities:
            ent.move(ent.x + ent.vx, ent.y + ent.vy)
            self.entity_collision(ent)

            if not ent.removeme:
                hits = self.world.entity_hitpos(ent)
                if hits:
                    for hit in hits:
                        ent.hit_world(self.world, hit)

            if ent.removeme:
                self.destroy(ent)

    def entity_collision(self, ent):
        for other in self.entities:
            if other != ent and ent.collides(other):
                other.hit(ent)

    def watch(self, entity):
        self.entities.append(entity)

    def destroy(self, entity):
        self.entities.remove(entity)

    def render(self, surf):
        for ent in self.entities:
            ent.render(surf)
