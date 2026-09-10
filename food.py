import random
import pygame


class Food:
    def __init__(self, width, height):

        self.block_size = 20

        self.width = width
        self.height = height

        self.position = self.random_position()

    def random_position(self):

        x = random.randrange(
            0,
            self.width,
            self.block_size
        )

        y = random.randrange(
            0,
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

    def draw(self, screen):

        x, y = self.position

        pygame.draw.rect(
            screen,
            (220, 60, 60),
            (
                x,
                y,
                self.block_size,
                self.block_size
            )
        )