import pygame


# Each glyph is a 5x7 grid. "X" is a filled pixel.
GLYPHS = {
    " ": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
    ),
    "A": (
        ".XXX.",
        "X...X",
        "X...X",
        "XXXXX",
        "X...X",
        "X...X",
        "X...X",
    ),
    "B": (
        "XXXX.",
        "X...X",
        "X...X",
        "XXXX.",
        "X...X",
        "X...X",
        "XXXX.",
    ),
    "C": (
        ".XXX.",
        "X...X",
        "X....",
        "X....",
        "X....",
        "X...X",
        ".XXX.",
    ),
    "D": (
        "XXXX.",
        "X...X",
        "X...X",
        "X...X",
        "X...X",
        "X...X",
        "XXXX.",
    ),
    "E": (
        "XXXXX",
        "X....",
        "X....",
        "XXXX.",
        "X....",
        "X....",
        "XXXXX",
    ),
    "F": (
        "XXXXX",
        "X....",
        "X....",
        "XXXX.",
        "X....",
        "X....",
        "X....",
    ),
    "G": (
        ".XXX.",
        "X...X",
        "X....",
        "X.XXX",
        "X...X",
        "X...X",
        ".XXX.",
    ),
    "H": (
        "X...X",
        "X...X",
        "X...X",
        "XXXXX",
        "X...X",
        "X...X",
        "X...X",
    ),
    "I": (
        "XXXXX",
        "..X..",
        "..X..",
        "..X..",
        "..X..",
        "..X..",
        "XXXXX",
    ),
    "J": (
        "..XXX",
        "...X.",
        "...X.",
        "...X.",
        "...X.",
        "X..X.",
        ".XX..",
    ),
    "K": (
        "X...X",
        "X..X.",
        "X.X..",
        "XX...",
        "X.X..",
        "X..X.",
        "X...X",
    ),
    "L": (
        "X....",
        "X....",
        "X....",
        "X....",
        "X....",
        "X....",
        "XXXXX",
    ),
    "M": (
        "X...X",
        "XX.XX",
        "X.X.X",
        "X.X.X",
        "X...X",
        "X...X",
        "X...X",
    ),
    "N": (
        "X...X",
        "XX..X",
        "X.X.X",
        "X.X.X",
        "X..XX",
        "X...X",
        "X...X",
    ),
    "O": (
        ".XXX.",
        "X...X",
        "X...X",
        "X...X",
        "X...X",
        "X...X",
        ".XXX.",
    ),
    "P": (
        "XXXX.",
        "X...X",
        "X...X",
        "XXXX.",
        "X....",
        "X....",
        "X....",
    ),
    "Q": (
        ".XXX.",
        "X...X",
        "X...X",
        "X...X",
        "X.X.X",
        "X..X.",
        ".XX.X",
    ),
    "R": (
        "XXXX.",
        "X...X",
        "X...X",
        "XXXX.",
        "X.X..",
        "X..X.",
        "X...X",
    ),
    "S": (
        ".XXXX",
        "X....",
        "X....",
        ".XXX.",
        "....X",
        "....X",
        "XXXX.",
    ),
    "T": (
        "XXXXX",
        "..X..",
        "..X..",
        "..X..",
        "..X..",
        "..X..",
        "..X..",
    ),
    "U": (
        "X...X",
        "X...X",
        "X...X",
        "X...X",
        "X...X",
        "X...X",
        ".XXX.",
    ),
    "V": (
        "X...X",
        "X...X",
        "X...X",
        "X...X",
        "X...X",
        ".X.X.",
        "..X..",
    ),
    "W": (
        "X...X",
        "X...X",
        "X...X",
        "X.X.X",
        "X.X.X",
        "XX.XX",
        "X...X",
    ),
    "X": (
        "X...X",
        "X...X",
        ".X.X.",
        "..X..",
        ".X.X.",
        "X...X",
        "X...X",
    ),
    "Y": (
        "X...X",
        "X...X",
        ".X.X.",
        "..X..",
        "..X..",
        "..X..",
        "..X..",
    ),
    "Z": (
        "XXXXX",
        "....X",
        "...X.",
        "..X..",
        ".X...",
        "X....",
        "XXXXX",
    ),
    "0": (
        ".XXX.",
        "X...X",
        "X..XX",
        "X.X.X",
        "XX..X",
        "X...X",
        ".XXX.",
    ),
    "1": (
        "..X..",
        ".XX..",
        "..X..",
        "..X..",
        "..X..",
        "..X..",
        "XXXXX",
    ),
    "2": (
        ".XXX.",
        "X...X",
        "....X",
        "...X.",
        "..X..",
        ".X...",
        "XXXXX",
    ),
    "3": (
        "XXXXX",
        "...X.",
        "..X..",
        "...X.",
        "....X",
        "X...X",
        ".XXX.",
    ),
    "4": (
        "...X.",
        "..XX.",
        ".X.X.",
        "X..X.",
        "XXXXX",
        "...X.",
        "...X.",
    ),
    "5": (
        "XXXXX",
        "X....",
        "XXXX.",
        "....X",
        "....X",
        "X...X",
        ".XXX.",
    ),
    "6": (
        "..XX.",
        ".X...",
        "X....",
        "XXXX.",
        "X...X",
        "X...X",
        ".XXX.",
    ),
    "7": (
        "XXXXX",
        "....X",
        "...X.",
        "..X..",
        ".X...",
        ".X...",
        ".X...",
    ),
    "8": (
        ".XXX.",
        "X...X",
        "X...X",
        ".XXX.",
        "X...X",
        "X...X",
        ".XXX.",
    ),
    "9": (
        ".XXX.",
        "X...X",
        "X...X",
        ".XXXX",
        "....X",
        "...X.",
        ".XX..",
    ),
    ":": (
        ".....",
        "..X..",
        "..X..",
        ".....",
        "..X..",
        "..X..",
        ".....",
    ),
    ".": (
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        "..X..",
        "..X..",
    ),
    "-": (
        ".....",
        ".....",
        ".....",
        "XXXXX",
        ".....",
        ".....",
        ".....",
    ),
    "<": (
        "...X.",
        "..X..",
        ".X...",
        "X....",
        ".X...",
        "..X..",
        "...X.",
    ),
    ">": (
        ".X...",
        "..X..",
        "...X.",
        "....X",
        "...X.",
        "..X..",
        ".X...",
    ),
    "!": (
        "..X..",
        "..X..",
        "..X..",
        "..X..",
        "..X..",
        ".....",
        "..X..",
    ),
}

GLYPH_WIDTH = 5
GLYPH_HEIGHT = 7

# Blank columns between two glyphs, measured in font pixels.
LETTER_SPACING = 1


def text_size(text, scale, bold=False):
    """
    Pixel size of `text` when rendered at `scale`.
    """

    count = len(text)

    if count == 0:
        return (0, 0)

    # Bold thickens every stroke by one pixel to the right, so it
    # needs one more blank column between glyphs and one at the end.
    extra = 1 if bold else 0

    width = (
        count * GLYPH_WIDTH
        + (count - 1) * (LETTER_SPACING + extra)
        + extra
    )

    return (width * scale, GLYPH_HEIGHT * scale)


def render(text, scale, color, bold=False):
    """
    Render `text` as a blocky bitmap surface with a transparent
    background.
    """

    text = text.upper()

    width, height = text_size(text, scale, bold)

    surface = pygame.Surface(
        (max(width, 1), max(height, 1)),
        pygame.SRCALPHA
    )

    block_width = scale * 2 if bold else scale

    cursor = 0

    for char in text:

        glyph = GLYPHS.get(char, GLYPHS[" "])

        for row, line in enumerate(glyph):

            for column, pixel in enumerate(line):

                if pixel != "X":
                    continue

                pygame.draw.rect(
                    surface,
                    color,
                    (
                        (cursor + column) * scale,
                        row * scale,
                        block_width,
                        scale
                    )
                )

        cursor += GLYPH_WIDTH + LETTER_SPACING + (1 if bold else 0)

    return surface


def draw(screen, text, scale, color, center=None, topleft=None, bold=False):
    """
    Render `text` and blit it onto `screen`.

    Returns the rect it occupies.
    """

    surface = render(text, scale, color, bold)

    if center is not None:
        rect = surface.get_rect(center=center)
    else:
        rect = surface.get_rect(topleft=topleft)

    screen.blit(surface, rect)

    return rect
