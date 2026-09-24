"""
The rival snake's brain: head for the food, but never into a wall or
into itself.
"""

OPPOSITE = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT",
}


def next_direction(snake, target, field, avoid=(), danger=()):
    """
    Pick where the rival should turn next.

    `target` is the cell it wants (or None to just keep out of
    trouble). `avoid` holds cells it would rather not enter, such as
    the other snake's body, and `danger` holds cells it refuses to
    enter unless it has no other move at all, such as bombs.
    """

    block = snake.block_size

    moves = {
        "UP": (0, -block),
        "DOWN": (0, block),
        "LEFT": (-block, 0),
        "RIGHT": (block, 0),
    }

    head_x, head_y = snake.body[0]

    # The tail moves out of the way on the same step, so it is safe.
    own = set(snake.body[:-1])

    avoid = set(avoid)
    danger = set(danger)

    # Safe moves first, then the same list ignoring the other snake,
    # so a boxed-in rival still moves rather than freezing.
    for keep_clear in (avoid, set()):

        options = []

        for name, (dx, dy) in moves.items():

            if name == OPPOSITE[snake.direction]:
                continue

            cell = (head_x + dx, head_y + dy)

            if not field.collidepoint(cell):
                continue

            if cell in own or cell in keep_clear or cell in danger:
                continue

            if target is None:
                distance = 0
            else:
                distance = abs(cell[0] - target[0]) + abs(cell[1] - target[1])

            # Going straight on breaks ties, so it does not jitter.
            options.append((distance, name != snake.direction, name, cell))

        if options:
            return min(options)[2]

    return snake.direction
