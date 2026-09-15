import math

import pygame


class Snake:
    def __init__(self, width, height, head_color=None, body_color=None, top=0):

        self.block_size = 20

        self.head_color = head_color or (80, 220, 100)
        self.body_color = body_color or (50, 170, 80)

        # Starting position, snapped to the block grid so the snake can
        # always line up with the food.
        start_x = width // 2 // self.block_size * self.block_size
        start_y = (top + height) // 2 // self.block_size * self.block_size

        # Snake body
        self.body = [
            (start_x, start_y),
            (start_x - 20, start_y),
            (start_x - 40, start_y)
        ]

        # Where the body was before the last move, so drawing can
        # glide between the two instead of jumping a whole cell.
        self.previous_body = list(self.body)

        # Direction
        self.direction = "RIGHT"

        # Next direction
        self.next_direction = "RIGHT"

        # Counts moves, and drives the slither wave.
        self.steps = 0

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

        self.previous_body = list(self.body)

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

        self.steps += 1

    def grow(self, count=1):

        # Add blocks to the tail
        tail = self.body[-1]

        for _ in range(count):
            self.body.append(tail)

    def get_head_position(self):

        return self.body[0]

    def check_collision(self, width, height, top=0):

        head_x, head_y = self.body[0]

        # Wall collision
        if (
            head_x < 0
            or head_x >= width
            or head_y < top
            or head_y >= height
        ):
            return True

        # Self collision
        if self.body[0] in self.body[1:]:
            return True

        return False

    def spine(self, progress):
        """
        Centre of every body segment, slid `progress` of the way from
        where it was to where it is, with a slither wave applied
        across the body.
        """

        half = self.block_size / 2

        previous = self.previous_body

        points = []

        for index, (x, y) in enumerate(self.body):

            # After growing, the tail has no previous position yet.
            old_x, old_y = previous[min(index, len(previous) - 1)]

            points.append(
                (
                    old_x + (x - old_x) * progress + half,
                    old_y + (y - old_y) * progress + half
                )
            )

        phase = (self.steps + progress) * 0.9

        waved = []

        for index, (x, y) in enumerate(points):

            # Direction of the body at this point, used to push the
            # wave out sideways.
            ahead = points[max(index - 1, 0)]
            behind = points[min(index + 1, len(points) - 1)]

            dx = ahead[0] - behind[0]
            dy = ahead[1] - behind[1]

            length = math.hypot(dx, dy)

            if length == 0:
                waved.append((x, y))
                continue

            # The head barely sways; the body swings more.
            ramp = min(1.0, index / 3.0)

            offset = 5.5 * ramp * math.sin(index * 0.8 - phase)

            waved.append(
                (
                    x + (-dy / length) * offset,
                    y + (dx / length) * offset
                )
            )

        return waved

    def girth(self):
        """
        The snake thickens as it grows longer.
        """

        return 1.0 + min(0.25, (len(self.body) - 3) * 0.008)

    def radius_at(self, t):
        """
        Body thickness, from the head (t=0) to the tail tip (t=1).
        """

        half = self.block_size / 2 * self.girth()

        # Full bodied most of the way, tapering to a point at the tail.
        return max(3.0, half * (1.0 - 0.72 * t ** 2.2))

    def draw(self, screen, progress=1.0):

        points = self.spine(progress)

        path = densify(points, spacing=2.5)

        last = len(path) - 1

        # Dark outline first, then the body on top, so the outline
        # never covers the fill.
        outline = shade(self.body_color, 0.45)

        head_radius = self.block_size * 0.62 * self.girth()

        for index, (x, y) in enumerate(path):

            t = index / last if last else 0.0

            pygame.draw.circle(
                screen,
                outline,
                (int(x), int(y)),
                int(self.radius_at(t) + 1.5)
            )

        pygame.draw.circle(
            screen,
            outline,
            (int(path[0][0]), int(path[0][1])),
            int(head_radius + 1.5)
        )

        for index, (x, y) in enumerate(path):

            t = index / last if last else 0.0

            color = self.head_color if t < 0.10 else self.body_color

            pygame.draw.circle(
                screen,
                color,
                (int(x), int(y)),
                int(self.radius_at(t))
            )

        pygame.draw.circle(
            screen,
            self.head_color,
            (int(path[0][0]), int(path[0][1])),
            int(head_radius)
        )

        # Scale pattern down the back
        highlight = shade(self.body_color, 1.35)

        for index in range(6, last, 9):

            t = index / last

            x, y = path[index]

            pygame.draw.circle(
                screen,
                highlight,
                (int(x), int(y)),
                max(1, int(self.radius_at(t) * 0.35))
            )

        self.draw_head(screen, path)

    def draw_head(self, screen, path):

        head_x, head_y = path[0]

        # Facing direction, taken from the first stretch of body.
        neck = path[min(6, len(path) - 1)]

        dx = head_x - neck[0]
        dy = head_y - neck[1]

        length = math.hypot(dx, dy)

        if length == 0:
            dx, dy, length = 1.0, 0.0, 1.0

        dx /= length
        dy /= length

        # Perpendicular, for placing the eyes either side.
        px, py = -dy, dx

        for side in (-1, 1):

            eye_x = head_x + dx * 2.0 + px * 5.0 * side
            eye_y = head_y + dy * 2.0 + py * 5.0 * side

            pygame.draw.circle(screen, (250, 250, 240), (int(eye_x), int(eye_y)), 3)

            pygame.draw.circle(
                screen,
                (15, 15, 15),
                (int(eye_x + dx * 1.2), int(eye_y + dy * 1.2)),
                2
            )

        # Tongue, flicked out every other beat.
        if self.steps % 4 < 2:

            tip_x = head_x + dx * 20
            tip_y = head_y + dy * 20

            root_x = head_x + dx * 11
            root_y = head_y + dy * 11

            pygame.draw.line(
                screen,
                (230, 60, 90),
                (int(root_x), int(root_y)),
                (int(tip_x), int(tip_y)),
                2
            )

            for side in (-1, 1):

                pygame.draw.line(
                    screen,
                    (230, 60, 90),
                    (int(tip_x), int(tip_y)),
                    (int(tip_x + dx * 3 + px * 3 * side),
                     int(tip_y + dy * 3 + py * 3 * side)),
                    2
                )


def densify(points, spacing):
    """
    Walk the polyline and drop a point every `spacing` pixels, so the
    body can be drawn as a smooth run of circles.
    """

    if len(points) < 2:
        return list(points)

    path = []

    for index in range(len(points) - 1):

        x1, y1 = points[index]
        x2, y2 = points[index + 1]

        distance = math.hypot(x2 - x1, y2 - y1)

        count = max(1, int(distance / spacing))

        for step in range(count):

            t = step / count

            path.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t))

    path.append(points[-1])

    return path


def shade(color, factor):
    """
    Lighten (factor > 1) or darken (factor < 1) a colour.
    """

    return tuple(min(255, max(0, int(channel * factor))) for channel in color)
