import pygame

import pixelfont
from theme import BACKGROUND, INK


LINES = [
    "R TO RESTART",
    "P TO PAUSE",
    "ESC TO BACK HOMEPAGE",
    "Q TO QUIT",
    "S FOR SETTING",
]


class InstructionsPage:
    """
    The instruction page: the key list, and BACK.
    """

    def __init__(self, screen):

        self.screen = screen

        width = screen.get_width()
        height = screen.get_height()

        margin = 100

        self.title_topleft = (margin, 105)

        self.divider_y = 170
        self.divider_left = margin
        self.divider_right = width - margin

        self.line_x = margin
        self.first_line_y = 215
        self.line_spacing = 48

        back_width, back_height = pixelfont.text_size("< BACK", 2, bold=True)

        self.back_rect = pygame.Rect(
            margin,
            height - 120,
            back_width + 20,
            back_height + 14
        )

    def handle_event(self, event):
        """
        Returns "back" when the player leaves the page, else None.
        """

        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.KEYDOWN:

            if event.key in (
                pygame.K_ESCAPE,
                pygame.K_RETURN,
                pygame.K_KP_ENTER,
                pygame.K_SPACE,
                pygame.K_BACKSPACE
            ):
                return "back"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.back_rect.collidepoint(event.pos):
                return "back"

        return None

    def draw(self):

        self.screen.fill(BACKGROUND)

        pixelfont.draw(
            self.screen,
            "INSTRUCTIONS",
            5,
            INK,
            topleft=self.title_topleft,
            bold=True
        )

        pygame.draw.line(
            self.screen,
            INK,
            (self.divider_left, self.divider_y),
            (self.divider_right, self.divider_y),
            4
        )

        y = self.first_line_y

        for line in LINES:

            pixelfont.draw(
                self.screen,
                line,
                3,
                INK,
                topleft=(self.line_x, y),
                bold=True
            )

            y += self.line_spacing

        # BACK is always highlighted: it is the only control here.
        pygame.draw.rect(self.screen, INK, self.back_rect)

        pixelfont.draw(
            self.screen,
            "< BACK",
            2,
            BACKGROUND,
            center=self.back_rect.center,
            bold=True
        )
