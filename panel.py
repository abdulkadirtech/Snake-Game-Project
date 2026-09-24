import pygame

import pixelfont
from theme import BACKGROUND, INK


class PanelPage:
    """
    A bordered panel over the frozen game: a title, the score, one
    main button, and QUIT in the corner. Used for both PAUSED and
    GAME OVER.
    """

    def __init__(self, screen, title, button_label, button_action, shortcuts):

        self.screen = screen
        self.title = title
        self.shortcuts = shortcuts

        self.panel = pygame.Rect(0, 0, 500, 370)

        self.panel.center = (
            screen.get_width() // 2,
            screen.get_height() // 2
        )

        self.title_center = (self.panel.centerx, self.panel.top + 60)

        self.divider_y = self.panel.top + 103

        button_width, button_height = pixelfont.text_size(
            button_label, 3, bold=True
        )

        self.button_rect = pygame.Rect(
            0,
            0,
            button_width + 36,
            button_height + 22
        )

        self.button_rect.center = (self.panel.centerx, self.panel.top + 250)

        quit_width, quit_height = pixelfont.text_size("QUIT", 2, bold=True)

        self.quit_rect = pygame.Rect(
            self.panel.right - 30 - quit_width - 20,
            self.panel.bottom - 28 - quit_height - 14,
            quit_width + 20,
            quit_height + 14
        )

        self.items = [
            (button_action, button_label, self.button_rect, 3),
            ("quit", "QUIT", self.quit_rect, 2),
        ]

        self.selected = 0

    def handle_event(self, event):
        """
        Returns the chosen action, else None.
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

            elif event.key in self.shortcuts:
                return self.shortcuts[event.key]

        if event.type == pygame.MOUSEMOTION:

            for index, (_, _, rect, _) in enumerate(self.items):

                if rect.collidepoint(event.pos):
                    self.selected = index

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            for action, _, rect, _ in self.items:

                if rect.collidepoint(event.pos):
                    return action

        return None

    def score_lines(self, score, rival_score, show_result):
        """
        What to print between the divider and the button.
        """

        if rival_score is None:
            return [f"SCORE: {score}"]

        lines = [f"YOU: {score}", f"RIVAL: {rival_score}"]

        # Only once the game is actually over, and never on a draw.
        if show_result and score != rival_score:
            lines.insert(0, "YOU WON" if score > rival_score else "YOU LOST")

        return lines

    def draw(self, score, rival_score=None, show_result=False):

        # Dim the game behind the panel.
        shade = pygame.Surface(self.screen.get_size())
        shade.set_alpha(190)
        shade.fill(BACKGROUND)
        self.screen.blit(shade, (0, 0))

        pygame.draw.rect(self.screen, BACKGROUND, self.panel)
        pygame.draw.rect(self.screen, INK, self.panel, 4)

        pixelfont.draw(
            self.screen,
            self.title,
            5,
            INK,
            center=self.title_center,
            bold=True
        )

        pygame.draw.line(
            self.screen,
            INK,
            (self.panel.left + 30, self.divider_y),
            (self.panel.right - 30, self.divider_y),
            4
        )

        lines = self.score_lines(score, rival_score, show_result)

        # Centre the block of lines in the gap between the divider and
        # the button, so one line or three both sit comfortably.
        spacing = 34
        middle = (self.divider_y + self.button_rect.top) // 2
        top = middle - (len(lines) - 1) * spacing // 2

        for index, line in enumerate(lines):

            pixelfont.draw(
                self.screen,
                line,
                3,
                INK,
                center=(self.panel.centerx, top + index * spacing),
                bold=True
            )

        for index, (_, label, rect, scale) in enumerate(self.items):

            if index == self.selected:
                pygame.draw.rect(self.screen, INK, rect)
                text_color = BACKGROUND
            else:
                text_color = INK

            if rect is self.button_rect:
                pygame.draw.rect(self.screen, INK, rect, 4)

            pixelfont.draw(
                self.screen,
                label,
                scale,
                text_color,
                center=rect.center,
                bold=True
            )
