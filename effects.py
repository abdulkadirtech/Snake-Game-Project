import math
import random

import pygame


DURATION = 550


class Explosion:
    """
    The flash left behind by a bomb that was never eaten.
    """

    def __init__(self, center):

        self.center = center
        self.started_at = pygame.time.get_ticks()

        self.sparks = [
            (
                random.uniform(0, math.tau),
                random.uniform(34, 62)
            )
            for _ in range(14)
        ]

    def finished(self):

        return pygame.time.get_ticks() - self.started_at > DURATION

    def draw(self, screen):

        age = (pygame.time.get_ticks() - self.started_at) / DURATION

        if age > 1:
            return

        center_x, center_y = self.center

        # Expanding shock ring
        radius = int(8 + 46 * age)

        pygame.draw.circle(
            screen,
            (255, 180, 50),
            (center_x, center_y),
            radius,
            max(1, int(5 * (1 - age)))
        )

        # Fireball, shrinking as it fades
        core = int(18 * (1 - age))

        if core > 0:
            pygame.draw.circle(screen, (255, 120, 30), (center_x, center_y), core)
            pygame.draw.circle(
                screen,
                (255, 235, 140),
                (center_x, center_y),
                max(1, core // 2)
            )

        # Flying sparks
        for angle, speed in self.sparks:

            distance = speed * age

            pygame.draw.circle(
                screen,
                (255, 200, 80),
                (
                    int(center_x + math.cos(angle) * distance),
                    int(center_y + math.sin(angle) * distance)
                ),
                max(1, int(4 * (1 - age)))
            )
