"""
Draws docs/structure.png: the repository laid out as a tree, grouped by
what each file is for, in the game's colours.
"""

import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame

pygame.init()

BG = (0, 0, 0)
INK = (70, 220, 80)
DIM = (122, 179, 129)
LINE = (40, 110, 50)
ORANGE = (250, 165, 60)
BLUE = (95, 175, 255)

title_font = pygame.font.SysFont("consolas", 34, bold=True)
group_font = pygame.font.SysFont("consolas", 19, bold=True)
file_font = pygame.font.SysFont("consolas", 21, bold=True)
desc_font = pygame.font.SysFont("consolas", 18)
note_font = pygame.font.SysFont("consolas", 17)

# (group label, colour, [(name, description), ...])
GROUPS = [
    ("ENTRY", ORANGE, [
        ("main.py", "starts Pygame and runs the Game"),
    ]),
    ("GAME LOGIC", INK, [
        ("game.py", "main loop, screens, input, score, speed, timer"),
        ("snake.py", "body, movement, collisions, slither drawing"),
        ("ai.py", "the rival snake's steering in two-snake mode"),
        ("food.py", "apple, mango, watermelon, kiwi, gold, bomb"),
        ("effects.py", "the bomb explosion"),
    ]),
    ("PAGES", INK, [
        ("menu.py", "home page: START, SETTING, QUIT"),
        ("settings.py", "sound, colour, players, timer, instructions"),
        ("instructions.py", "the key list"),
        ("panel.py", "PAUSED and GAME OVER panels"),
        ("ui.py", "score bar and match clock"),
    ]),
    ("LOOK AND SOUND", INK, [
        ("pixelfont.py", "bitmap font drawn from 5x7 grids"),
        ("theme.py", "colours, canvas size, score-bar height"),
        ("audio.py", "beep, explosion and music, generated at startup"),
    ]),
    ("TESTS AND DOCS", BLUE, [
        ("test_game.py", "automated checks  (python test_game.py)"),
        ("README.md", "how to run, controls, structure"),
        ("docs/", "flowchart and structure diagrams"),
    ]),
]

LEFT = 60
TOP = 100
ROW = 32
GROUP_GAP = 26
TREE_X = LEFT + 40
NAME_X = TREE_X + 36
DESC_X = NAME_X + 200

W = 1100
H = TOP + sum(len(files) * ROW + GROUP_GAP + 30 for _, _, files in GROUPS) + 80

surface = pygame.Surface((W, H))
surface.fill(BG)


def blit(font, string, color, pos):
    surface.blit(font.render(string, True, color), pos)


blit(title_font, "Snake Game - Repository Structure", INK, (LEFT, 30))

# root
blit(file_font, "snake/", ORANGE, (LEFT, TOP - 34))

y = TOP
last_y = y

for label, color, files in GROUPS:

    blit(group_font, label, DIM, (NAME_X, y))
    y += 30

    for name, desc in files:

        row_mid = y + ROW // 2 - 2

        # branch from the trunk
        pygame.draw.line(surface, LINE, (TREE_X, row_mid), (NAME_X - 12, row_mid), 2)

        blit(file_font, name, color, (NAME_X, y))
        blit(desc_font, desc, DIM, (DESC_X, y + 2))

        last_y = row_mid
        y += ROW

    y += GROUP_GAP

# trunk, drawn last so it sits under every branch
pygame.draw.line(surface, LINE, (TREE_X, TOP - 8), (TREE_X, last_y), 2)

notes = [
    "__pycache__/ is created by Python when the game runs and is not part of the project.",
    "game.py only coordinates - each module owns its own data and drawing.",
]

y += 4
for line in notes:
    blit(note_font, line, DIM, (LEFT, y))
    y += 26

out = os.path.join(
    r"C:\Users\abdul\Desktop\Projects\Snake Game\snake", "docs", "structure.png"
)
pygame.image.save(surface, out)
print(out)
