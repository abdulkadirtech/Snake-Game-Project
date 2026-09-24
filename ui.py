import pygame

import pixelfont
from theme import INK, HUD_HEIGHT


class UI:
    def __init__(self, screen):

        self.screen = screen

    def draw_score(self, score, time_left=None, rival_score=None):

        pixelfont.draw(
            self.screen,
            f"SCORE: {score}",
            3,
            INK,
            topleft=(20, 18),
            bold=True
        )

        # The rival's tally, only in two-snake mode.
        if rival_score is not None:

            pixelfont.draw(
                self.screen,
                f"RIVAL: {rival_score}",
                3,
                INK,
                center=(self.screen.get_width() // 2, HUD_HEIGHT // 2),
                bold=True
            )

        # Match clock, only when the TIMER setting is on.
        if time_left is not None:

            seconds = -(-time_left // 1000)

            pixelfont.draw(
                self.screen,
                f"TIME: {seconds}",
                3,
                INK,
                topleft=(self.screen.get_width() - 200, 18),
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
