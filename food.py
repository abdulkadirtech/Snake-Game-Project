import math
import random

import pygame


# name, points, spawn weight
FOOD_TYPES = [
    ("apple", 1, 20),
    ("mango", 1, 20),
    ("watermelon", 1, 20),
    ("kiwi", 1, 20),
    ("gold", 3, 7),
    # A bomb is never worth anything: eating one ends the game.
    ("bomb", 0, 9),
]

# Food left alone goes away and is replaced. Nothing stops the
# replacement being the same kind again.
DEFAULT_LIFETIME = 9000

LIFETIMES = {
    "gold": 6000,
    "bomb": 4000,
}

# How long a food blinks before it goes.
BLINK_FOR = 1200

NAMES = [name for name, _, _ in FOOD_TYPES]
WEIGHTS = [weight for _, _, weight in FOOD_TYPES]
POINTS = {name: points for name, points, _ in FOOD_TYPES}


class Food:
    def __init__(self, width, height, snake_body=None, top=0):

        self.block_size = 20

        self.width = width
        self.height = height

        # Food never spawns above this line, so it cannot end up
        # behind the score text.
        self.top = top

        # The very first food must also avoid the snake body,
        # otherwise it can spawn underneath the snake at startup
        # and the player simply cannot see it.
        if snake_body is None:
            snake_body = []

        self.kind = "apple"
        self.spawned_at = 0

        self.position = self.random_position()

        self.randomize(snake_body)

    @property
    def points(self):
        return POINTS[self.kind]

    def random_position(self):

        x = random.randrange(
            0,
            self.width,
            self.block_size
        )

        y = random.randrange(
            self.top,
            self.height,
            self.block_size
        )

        return (x, y)

    def randomize(self, snake_body):

        new_position = self.random_position()

        # Make sure food doesn't appear inside snake
        while new_position in snake_body:

            new_position = self.random_position()

        self.position = new_position

        self.kind = random.choices(NAMES, WEIGHTS)[0]

        self.spawned_at = pygame.time.get_ticks()

    @property
    def lifetime(self):

        return LIFETIMES.get(self.kind, DEFAULT_LIFETIME)

    def time_left(self):

        return self.lifetime - (pygame.time.get_ticks() - self.spawned_at)

    def expired(self):
        """
        True once this food has sat around uneaten for long enough.
        """

        return self.time_left() < 0

    def draw(self, screen):

        x, y = self.position

        # Food about to go blinks.
        left = self.time_left()

        if left < BLINK_FOR and (left // 150) % 2 == 0:
            return

        rect = pygame.Rect(
            x,
            y,
            self.block_size,
            self.block_size
        )

        DRAWERS[self.kind](screen, rect)


def draw_apple(screen, rect):

    body = rect.inflate(-3, -2)
    body.top = rect.top + 4

    pygame.draw.ellipse(screen, (215, 45, 45), body)
    pygame.draw.ellipse(screen, (255, 130, 120), body.inflate(-10, -10))

    # Stem and leaf
    pygame.draw.line(
        screen,
        (110, 70, 35),
        (rect.centerx, rect.top + 5),
        (rect.centerx, rect.top + 1),
        2
    )

    pygame.draw.ellipse(
        screen,
        (70, 180, 70),
        pygame.Rect(rect.centerx, rect.top + 1, 6, 4)
    )


def draw_mango(screen, rect):

    body = rect.inflate(-4, -3)

    pygame.draw.ellipse(screen, (240, 150, 40), body)
    pygame.draw.ellipse(
        screen,
        (250, 205, 70),
        pygame.Rect(body.left + 3, body.top + 3, 7, 6)
    )

    pygame.draw.ellipse(
        screen,
        (225, 80, 60),
        pygame.Rect(body.right - 8, body.top + 1, 6, 5)
    )

    pygame.draw.line(
        screen,
        (90, 140, 60),
        (rect.centerx + 2, rect.top + 3),
        (rect.centerx + 4, rect.top),
        2
    )


def draw_watermelon(screen, rect):
    """
    A slice: flat side up, rind curving underneath.
    """

    flat_y = rect.top + 5
    center_x = rect.centerx

    def half_disc(radius, top):

        return [
            (
                center_x + radius * math.cos(math.pi * step / 12),
                top + radius * math.sin(math.pi * step / 12)
            )
            for step in range(13)
        ]

    pygame.draw.polygon(screen, (60, 150, 60), half_disc(9, flat_y))
    pygame.draw.polygon(screen, (220, 240, 200), half_disc(7, flat_y))
    pygame.draw.polygon(screen, (230, 60, 70), half_disc(6, flat_y))

    for x_offset, y_offset in ((-3, 2), (2, 2), (0, 5)):

        pygame.draw.circle(
            screen,
            (25, 25, 25),
            (center_x + x_offset, flat_y + y_offset),
            1
        )


def draw_kiwi(screen, rect):

    center = rect.center
    radius = rect.width // 2 - 1

    pygame.draw.circle(screen, (120, 85, 45), center, radius)
    pygame.draw.circle(screen, (140, 200, 80), center, radius - 2)
    pygame.draw.circle(screen, (235, 240, 210), center, 3)

    for index in range(8):

        angle = index * math.pi / 4

        pygame.draw.circle(
            screen,
            (25, 25, 25),
            (
                int(center[0] + 5 * math.cos(angle)),
                int(center[1] + 5 * math.sin(angle))
            ),
            1
        )


def draw_gold(screen, rect):

    center = rect.center
    radius = rect.width // 2 - 1

    pygame.draw.circle(screen, (180, 130, 20), center, radius)
    pygame.draw.circle(screen, (255, 210, 60), center, radius - 2)
    pygame.draw.circle(screen, (200, 150, 25), center, radius - 5, 1)

    pygame.draw.line(
        screen,
        (255, 250, 200),
        (center[0] - 3, center[1] + 3),
        (center[0] + 2, center[1] - 4),
        2
    )


def draw_bomb(screen, rect):

    center = (rect.centerx, rect.centery + 2)
    radius = rect.width // 2 - 2

    pygame.draw.circle(screen, (35, 35, 40), center, radius)
    pygame.draw.circle(screen, (90, 90, 100), center, radius, 1)

    pygame.draw.circle(
        screen,
        (150, 150, 160),
        (center[0] - 3, center[1] - 3),
        2
    )

    # Fuse
    pygame.draw.line(
        screen,
        (150, 110, 60),
        (center[0] + 2, rect.top + 4),
        (rect.right - 3, rect.top + 1),
        2
    )

    pygame.draw.circle(screen, (255, 170, 40), (rect.right - 3, rect.top + 1), 2)


DRAWERS = {
    "apple": draw_apple,
    "mango": draw_mango,
    "watermelon": draw_watermelon,
    "kiwi": draw_kiwi,
    "gold": draw_gold,
    "bomb": draw_bomb,
}
