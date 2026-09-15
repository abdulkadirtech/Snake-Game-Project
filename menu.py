import pygame

import pixelfont
from theme import BACKGROUND, INK


class Menu:
    """
    The first page: title, START button, SETTING and QUIT.
    """

    def __init__(self, screen):

        self.screen = screen

        width = screen.get_width()
        height = screen.get_height()

        margin = 90

        # Title
        self.title_center = (width // 2, 150)

        # Divider under the title
        self.divider_y = 205
        self.divider_left = margin + 60
        self.divider_right = width - margin - 60

        # START button
        start_width, start_height = pixelfont.text_size("START", 5, bold=True)

        self.start_rect = pygame.Rect(
            0,
            0,
            start_width + 60,
            start_height + 34
        )

        self.start_rect.center = (width // 2, 300)

        # SETTING (bottom left) and QUIT (bottom right)
        setting_width, setting_height = pixelfont.text_size(
            "SETTING", 2, bold=True
        )

        self.setting_rect = pygame.Rect(
            margin,
            height - 120,
            setting_width + 20,
            setting_height + 14
        )

        quit_width, quit_height = pixelfont.text_size("QUIT", 2, bold=True)

        self.quit_rect = pygame.Rect(
            width - margin - quit_width - 20,
            self.setting_rect.top,
            quit_width + 20,
            quit_height + 14
        )

        self.items = [
            ("start", "START", self.start_rect, 5),
            ("setting", "SETTING", self.setting_rect, 2),
            ("quit", "QUIT", self.quit_rect, 2),
        ]

        self.selected = 0

    def handle_event(self, event):
        """
        Returns the chosen action ("start", "setting", "quit") or
        None while the player is still browsing.
        """

        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_UP, pygame.K_LEFT):
                self.selected = (self.selected - 1) % len(self.items)

            elif event.key in (pygame.K_DOWN, pygame.K_RIGHT):
                self.selected = (self.selected + 1) % len(self.items)

            elif event.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER,
                pygame.K_SPACE
            ):
                return self.items[self.selected][0]

            elif event.key == pygame.K_ESCAPE:
                return "quit"

        if event.type == pygame.MOUSEMOTION:

            for index, (_, _, rect, _) in enumerate(self.items):

                if rect.collidepoint(event.pos):
                    self.selected = index

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            for action, _, rect, _ in self.items:

                if rect.collidepoint(event.pos):
                    return action

        return None

    def draw(self):

        self.screen.fill(BACKGROUND)

        # Title
        pixelfont.draw(
            self.screen,
            "SNAKE GAME",
            7,
            INK,
            center=self.title_center,
            bold=True
        )

        # Divider under the title
        pygame.draw.line(
            self.screen,
            INK,
            (self.divider_left, self.divider_y),
            (self.divider_right, self.divider_y),
            4
        )

        # Menu items
        for index, (_, label, rect, scale) in enumerate(self.items):

            is_selected = index == self.selected

            if is_selected:
                # Inverted: filled box, background-coloured text.
                pygame.draw.rect(self.screen, INK, rect)
                text_color = BACKGROUND
            else:
                text_color = INK

            if label == "START":
                # The START box is always outlined, as in the design.
                pygame.draw.rect(self.screen, INK, rect, 4)

            pixelfont.draw(
                self.screen,
                label,
                scale,
                text_color,
                center=rect.center,
                bold=True
            )
