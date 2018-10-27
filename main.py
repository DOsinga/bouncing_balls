import colorsys

import math
import pygame
import random
from rtree import index


MIN_RADIUS = 15
MAX_RADIUS = 25

def random_color():
    hue = random.random()
    lightness = random.random() * 0.3 + 0.5
    saturation = random.random() * 0.2 + 0.7
    return tuple(map(lambda f: int(f * 255), colorsys.hls_to_rgb(hue, lightness, saturation)))


class Creature:
    """Creature class representing one bouncing ball for now."""
    id_count = 0

    def __init__(self, x, y, dx, dy, color, radius):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.radius = radius
        self.id = Creature.id_count
        Creature.id_count += 1

    def step(self, world, overlapping):
        self.x += self.dx
        self.y += self.dy

        ddx = random.random() * 0.3 - 0.15
        ddy = random.random() * 0.3 - 0.15

        # Bounce off walls:
        if self.x < self.radius:
            ddx -= self.x - self.radius
        elif self.x > world.width - self.radius:
            ddx += world.width - self.radius - self.x
        if self.y < self.radius:
            ddy -= self.y - self.radius
        elif self.y > world.height - self.radius:
            ddy += world.height - self.radius - self.y

        for other in overlapping:
            dist = self.distance(other.x, other.y)
            if dist:
                ddx -= 3 * (other.x - self.x) / dist
                ddy -= 3 * (other.y - self.y) / dist

        self.dx += ddx
        self.dy += ddy

        # Maximum speed:
        if abs(self.dx) > 7:
            self.dx *= 7 / abs(self.dx)
        if abs(self.dy) > 7:
            self.dy *= 7 / abs(self.dy)


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

    def box(self):
        """Return the bounding box for this creature"""
        r2 = self.radius
        res = [self.x - r2, self.y - r2, self.x + r2, self.y + r2]
        return res

    def distance(self, x1, y1):
        dx = self.x - x1
        dy = self.y - y1
        return math.sqrt(dx * dx + dy * dy)


class World:
    """The world and the creatures in it. Also has an r-tree for collision detection."""
    def __init__(self):
        self.index = index.Index()
        self.width = 640
        self.height = 480
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

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for creature in self.creatures.values():
            creature.draw(screen)

    def random_creature(self):
        radius = random.random() * MIN_RADIUS + (MAX_RADIUS - MIN_RADIUS)
        creature = Creature(random.random() * (self.width - radius * 2) + radius,
                            random.random() * (self.height - radius * 2) + radius,
                            random.random() * 14 - 2,
                            random.random() * 4 - 2,
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


def main():
    world = World()
 
    screen = pygame.display.set_mode((world.width, world.height))
 
    pygame.display.set_caption('Bouncing Balls')
 
    clock = pygame.time.Clock()

    for _ in range(50):
        world.add_creature(world.random_creature())

    while True:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                # Space bar! Spawn a new ball.
                if event.key == pygame.K_SPACE:
                    world.add_creature(world.random_creature())

        world.step()
        world.draw(screen)
        clock.tick(30)
        pygame.display.flip()

 
if __name__ == '__main__':
    pygame.init()
    try:
        main()
    finally:
        pygame.quit()

