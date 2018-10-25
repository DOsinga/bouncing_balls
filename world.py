import random
import colorsys
from rtree import index

from creature import Creature, MIN_RADIUS, MAX_RADIUS, MAX_SPEED



def random_color():
    hue = random.random()
    lightness = random.random() * 0.3 + 0.5
    saturation = random.random() * 0.2 + 0.7
    return tuple(map(lambda f: int(f * 255), colorsys.hls_to_rgb(hue, lightness, saturation)))


class World:
    """The world and the creatures in it. Also has an r-tree for collision detection."""
    def __init__(self, width=640, height=480):
        self.index = index.Index()
        self.width = width
        self.height = height
        self.creatures = {}

    def add_creature(self, creature):
        self.creatures[creature.id] = creature

    def del_creature(self, creature):
        del self.creatures[creature.id]

    def step(self):
        for creature in self.creatures.values():
            self.index.delete(creature.id, creature.box())
            creature.step(self, self.overlaps(creature))
            self.index.add(creature.id, creature.box())

    def draw(self, display):
        display.clear()
        for creature in self.creatures.values():
            creature.draw(display)

    def random_creature(self):
        max_y_speed = MAX_SPEED / self.width * self.height
        radius = random.random() * MIN_RADIUS + (MAX_RADIUS - MIN_RADIUS)
        creature = Creature(random.random() * (self.width - radius * 2) + radius,
                            random.random() * (self.height - radius * 2) + radius,
                            (random.random() * 2 -1) * MAX_SPEED,
                            (random.random() * 2 -1) * max_y_speed,
                            color=random_color(),
                            radius=radius)
        return creature

    def overlaps(self, creature):
        """Return any creature inside the circle (x,y) with the given radius."""
        res = []
        for candidate_id in self.index.intersection(creature.box()):
            candidate = self.creatures[candidate_id]
            if creature.distance(candidate.x, candidate.y) < candidate.radius + creature.radius:
                res.append(candidate)
        return res
