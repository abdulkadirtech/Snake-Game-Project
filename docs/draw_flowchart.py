"""
Draws docs/flowchart.png for the Snake game.
"""

import math
import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame

pygame.init()

W, H = 1280, 860
BG = (0, 0, 0)
INK = (70, 220, 80)
GREEN = (70, 220, 80)
GREEN_FILL = (10, 20, 11)
ORANGE = (250, 165, 60)
ORANGE_FILL = (26, 16, 4)
RED = (230, 80, 60)
GREY = (122, 179, 129)

surface = pygame.Surface((W, H))
surface.fill(BG)

title_font = pygame.font.SysFont("consolas", 34, bold=True)
box_font = pygame.font.SysFont("consolas", 24, bold=True)
sub_font = pygame.font.SysFont("consolas", 17)
label_font = pygame.font.SysFont("consolas", 18, bold=True)
note_font = pygame.font.SysFont("consolas", 17)


def text(font, string, color):
    return font.render(string, True, color)


# ---- boxes -----------------------------------------------------------

boxes = {}


def box(name, center, label, sub=None, color=GREEN, fill=GREEN_FILL, round_=False):

    main = text(box_font, label, INK)

    width = max(200, main.get_width() + 50)

    if sub:
        width = max(width, text(sub_font, sub, GREY).get_width() + 30)
    height = 68 if sub else 56

    rect = pygame.Rect(0, 0, width, height)
    rect.center = center

    radius = rect.height // 2 if round_ else 6

    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    pygame.draw.rect(surface, color, rect, 3, border_radius=radius)

    if sub:
        surface.blit(main, main.get_rect(center=(rect.centerx, rect.centery - 11)))
        small = text(sub_font, sub, GREY)
        surface.blit(small, small.get_rect(center=(rect.centerx, rect.centery + 15)))
    else:
        surface.blit(main, main.get_rect(center=rect.center))

    boxes[name] = rect


box("home", (640, 110), "SNAKE GAME", "home page")
box("setting", (240, 300), "SETTING", "sound, colour, players, timer")
box("instructions", (250, 500), "INSTRUCTIONS")
box("game", (640, 300), "GAME", "playing")
box("paused", (470, 520), "PAUSED")
box("over", (810, 520), "GAME OVER")
box("exit", (1090, 520), "EXIT", None, ORANGE, ORANGE_FILL, round_=True)


# ---- arrows ----------------------------------------------------------

def edge_point(rect, toward):
    """
    Where a line from the rect's centre toward `toward` leaves the rect.
    """

    cx, cy = rect.center
    dx, dy = toward[0] - cx, toward[1] - cy

    if dx == 0 and dy == 0:
        return rect.center

    scale = min(
        (rect.width / 2) / abs(dx) if dx else math.inf,
        (rect.height / 2) / abs(dy) if dy else math.inf,
    )

    return (cx + dx * scale, cy + dy * scale)


def arrowhead(tip, from_point, color):

    angle = math.atan2(tip[1] - from_point[1], tip[0] - from_point[0])
    size = 13

    points = [
        tip,
        (tip[0] - size * math.cos(angle - 0.45), tip[1] - size * math.sin(angle - 0.45)),
        (tip[0] - size * math.cos(angle + 0.45), tip[1] - size * math.sin(angle + 0.45)),
    ]

    pygame.draw.polygon(surface, color, points)


def label_at(point, string, color):

    surf = text(label_font, string, color)
    rect = surf.get_rect(center=point)
    pygame.draw.rect(surface, BG, rect.inflate(10, 4))
    surface.blit(surf, rect)


def arrow(start, end, label, color=INK, offset=0, label_shift=(0, 0)):
    """
    Straight arrow between two boxes. `offset` slides the line sideways
    so two arrows between the same boxes do not overlap.
    """

    a = boxes[start]
    b = boxes[end]

    dx, dy = b.centerx - a.centerx, b.centery - a.centery
    length = math.hypot(dx, dy)
    nx, ny = -dy / length * offset, dx / length * offset

    ca = (a.centerx + nx, a.centery + ny)
    cb = (b.centerx + nx, b.centery + ny)

    shifted_a = a.move(nx, ny)
    shifted_b = b.move(nx, ny)

    p1 = edge_point(shifted_a, cb)
    p2 = edge_point(shifted_b, ca)

    pygame.draw.line(surface, color, p1, p2, 3)
    arrowhead(p2, p1, color)

    mid = ((p1[0] + p2[0]) / 2 + label_shift[0], (p1[1] + p2[1]) / 2 + label_shift[1])
    label_at(mid, label, color)


def elbow(points, label, color=INK, label_index=1):

    pygame.draw.lines(surface, color, False, points, 3)
    arrowhead(points[-1], points[-2], color)

    a, b = points[label_index], points[label_index + 1]
    label_at(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), label, color)


# home
arrow("home", "game", "START")
arrow("home", "setting", "SETTING", offset=-14, label_shift=(-70, -26))
h = boxes["home"]
elbow([(h.right, h.centery), (boxes["exit"].centerx, h.centery), (boxes["exit"].centerx, boxes["exit"].top - 2)], "QUIT", ORANGE, label_index=0)

# setting
arrow("setting", "home", "BACK", offset=-14, label_shift=(62, 30))
arrow("setting", "instructions", "KEYBOARD INSTRUCTIONS", offset=-14, label_shift=(-136, 0))
arrow("instructions", "setting", "BACK", offset=-14, label_shift=(46, 0))

# game
arrow("game", "paused", "P  pause", offset=-14, label_shift=(-70, -6))
arrow("paused", "game", "RESUME", offset=-14, label_shift=(62, 14))
arrow("game", "over", "dies / time up", RED, offset=-14, label_shift=(80, -10))
arrow("over", "game", "REPLAY", offset=-14, label_shift=(-62, 14))

# restart loop on the right of GAME
g = boxes["game"]
loop = [
    (g.right, g.centery - 12),
    (g.right + 60, g.centery - 12),
    (g.right + 60, g.centery + 12),
    (g.right + 2, g.centery + 12),
]
pygame.draw.lines(surface, INK, False, loop, 3)
arrowhead(loop[-1], loop[-2], INK)
label_at((g.right + 96, g.centery), "R restart", INK)

# panels -> exit
arrow("over", "exit", "QUIT", ORANGE, label_shift=(0, -14))

p = boxes["paused"]
e = boxes["exit"]
elbow(
    [(p.centerx, p.bottom), (p.centerx, 640), (e.centerx, 640), (e.centerx, e.bottom + 2)],
    "QUIT",
    ORANGE,
    label_index=1,
)

# ---- title and notes -------------------------------------------------

surface.blit(text(title_font, "Snake Game - Flowchart", INK), (40, 28))

notes = [
    "Q quits from every menu and panel.  Esc = BACK on a menu, RESUME on PAUSED, home page on GAME OVER.",
    "During play only the arrow keys, P (pause) and R (restart) do anything.",
    "START, REPLAY and R begin a fresh game.  RESUME continues the one you were playing.",
    "GAME OVER comes from hitting a wall, biting yourself, eating a bomb, or the timer running out.",
]

y = 710
for line in notes:
    surface.blit(text(note_font, line, GREY), (40, y))
    y += 28

out = os.path.join(
    r"C:\Users\abdul\Desktop\Projects\Snake Game\snake", "docs", "flowchart.png"
)
os.makedirs(os.path.dirname(out), exist_ok=True)
pygame.image.save(surface, out)
print(out)
