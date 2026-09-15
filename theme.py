# Shared look: green text on a black screen.

BACKGROUND = (0, 0, 0)
INK = (70, 220, 80)
DIM = (32, 100, 40)

# Selectable snake colours: (name, head, body)
SNAKE_COLORS = [
    ("GREEN", (80, 220, 100), (50, 170, 80)),
    ("ORANGE", (250, 165, 60), (205, 120, 25)),
    ("BLUE", (95, 175, 255), (45, 115, 210)),
]

# Logical resolution everything is drawn at. The window can be any
# size; the canvas is scaled to fit it.
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

# Height of the score bar. The play field starts below it, so food
# never lands behind the score text.
HUD_HEIGHT = 60
