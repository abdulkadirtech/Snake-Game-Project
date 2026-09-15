import pygame

import pixelfont
from theme import INK, HUD_HEIGHT


class UI:
    def __init__(self, screen):

        self.screen = screen

    def draw_score(self, score):

        pixelfont.draw(
            self.screen,
            f"SCORE: {score}",
            3,
            INK,
            topleft=(20, 18),
            bold=True
        )

        # Line closing off the score bar.
        pygame.draw.line(
            self.screen,
            INK,
            (0, HUD_HEIGHT),
            (self.screen.get_width(), HUD_HEIGHT),
            3
        )
