import pygame

from display import Display
from world import World

START_NUM_CREATURES = 50
FRAME_RATE = 30

def main():
    world = World()
 
    display = Display("Bouncing Balls", world.width, world.height)
    clock = pygame.time.Clock()

    for _ in range(START_NUM_CREATURES):
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
        world.draw(display)
        clock.tick(FRAME_RATE)
        pygame.display.flip()

 
if __name__ == '__main__':
    pygame.init()
    try:
        main()
    finally:
        pygame.quit()

