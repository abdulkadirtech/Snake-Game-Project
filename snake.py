import pygame


class Snake:
    def __init__(self, width, height):

        self.block_size = 20

        # Starting position
        start_x = width // 2
        start_y = height // 2

        # Snake body
        self.body = [
            (start_x, start_y),
            (start_x - 20, start_y),
            (start_x - 40, start_y)
        ]

        # Direction
        self.direction = "RIGHT"

        # Next direction
        self.next_direction = "RIGHT"

    def change_direction(self, direction):

        # Prevent snake from immediately turning back.
        #
        # Note: we compare against self.direction (the direction
        # actually committed by the last move()), NOT next_direction.
        # This is deliberate -- it also blocks the case where the
        # player presses two keys inside a single frame, e.g.
        # moving RIGHT and pressing UP then LEFT before the next
        # move(): LEFT is rejected because direction is still RIGHT.

        if direction == "UP" and self.direction != "DOWN":
            self.next_direction = "UP"

        elif direction == "DOWN" and self.direction != "UP":
            self.next_direction = "DOWN"

        elif direction == "LEFT" and self.direction != "RIGHT":
            self.next_direction = "LEFT"

        elif direction == "RIGHT" and self.direction != "LEFT":
            self.next_direction = "RIGHT"

    def move(self):

        self.direction = self.next_direction

        head_x, head_y = self.body[0]

        if self.direction == "UP":
            head_y -= self.block_size

        elif self.direction == "DOWN":
            head_y += self.block_size

        elif self.direction == "LEFT":
            head_x -= self.block_size

        elif self.direction == "RIGHT":
            head_x += self.block_size

        new_head = (head_x, head_y)

        # Add new head
        self.body.insert(0, new_head)

        # Remove tail
        self.body.pop()

    def grow(self):

        # Add one more block to the tail
        tail = self.body[-1]

        self.body.append(tail)

    def get_head_position(self):

        return self.body[0]

    def check_collision(self, width, height):

        head_x, head_y = self.body[0]

        # Wall collision
        if (
            head_x < 0
            or head_x >= width
            or head_y < 0
            or head_y >= height
        ):
            return True

        # Self collision
        if self.body[0] in self.body[1:]:
            return True

        return False

    def draw(self, screen):

        for index, (x, y) in enumerate(self.body):

            if index == 0:
                # Head
                pygame.draw.rect(
                    screen,
                    (80, 220, 100),
                    (
                        x,
                        y,
                        self.block_size,
                        self.block_size
                    )
                )

            else:
                # Body
                pygame.draw.rect(
                    screen,
                    (50, 170, 80),
                    (
                        x,
                        y,
                        self.block_size,
                        self.block_size
                    )
                )