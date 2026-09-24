import random

import pygame

import pixelfont
from theme import BACKGROUND, INK, DIM, SNAKE_COLORS


# Rows that are a row of little boxes: label, choices, and the value
# each choice stands for.
OPTION_ROWS = {
    "sound": ("SOUND", [("ON", True), ("OFF", False)]),
    "players": ("PLAYERS MODE", [("1", 1), ("2", 2)]),
    "timer": ("TIMER", [("OFF", 0), ("60", 60), ("90", 90)]),
}


class Settings:
    """
    Player preferences, shared between the pages and the game.
    """

    def __init__(self):

        self.sound = True
        self.color_index = 0

        # 1 is the normal single-snake game.
        self.players = 1

        # Seconds on the clock, or 0 for no time limit.
        self.timer = 0

        # Re-rolled at the start of every two-snake game.
        self.rival_index = 1

    @property
    def head_color(self):
        return SNAKE_COLORS[self.color_index][1]

    @property
    def body_color(self):
        return SNAKE_COLORS[self.color_index][2]

    def pick_rival_color(self):
        """
        Give the rival a fresh colour: a random pick of the two the
        player is not using.
        """

        self.rival_index = random.choice(
            [
                index
                for index in range(len(SNAKE_COLORS))
                if index != self.color_index
            ]
        )

    @property
    def rival_head_color(self):
        return SNAKE_COLORS[self.rival_index][1]

    @property
    def rival_body_color(self):
        return SNAKE_COLORS[self.rival_index][2]


class SettingsPage:
    """
    The setting page: sound, snake colour, players, timer, keyboard
    instructions, back.
    """

    def __init__(self, screen, settings):

        self.screen = screen
        self.settings = settings

        width = screen.get_width()
        height = screen.get_height()

        margin = 100

        self.title_topleft = (margin, 105)

        self.divider_y = 170
        self.divider_left = margin
        self.divider_right = width - margin

        self.label_x = margin
        self.value_x = margin + 360

        self.rows = ["sound", "color", "players", "timer", "keyboard", "back"]

        self.row_spacing = 58

        self.row_y = {
            name: 215 + index * self.row_spacing
            for index, name in enumerate(self.rows[:-1])
        }

        # A row of boxes for each option row
        self.option_rects = {}

        for name, (_, choices) in OPTION_ROWS.items():

            x = self.value_x
            rects = []

            for label, _ in choices:

                box_width, box_height = pixelfont.text_size(label, 2, bold=True)

                rect = pygame.Rect(
                    x,
                    self.row_y[name] - (box_height + 14) // 2,
                    box_width + 20,
                    box_height + 14
                )

                rects.append(rect)

                x = rect.right + 6

            self.option_rects[name] = rects

        # Colour swatches
        swatch_size = 34

        self.swatch_rects = [
            pygame.Rect(
                self.value_x + index * (swatch_size + 16),
                self.row_y["color"] - swatch_size // 2,
                swatch_size,
                swatch_size
            )
            for index in range(len(SNAKE_COLORS))
        ]

        # BACK, same size as the first page's small buttons
        back_width, back_height = pixelfont.text_size("< BACK", 2, bold=True)

        self.back_rect = pygame.Rect(
            margin,
            height - 100,
            back_width + 20,
            back_height + 14
        )

        self.selected = 0

    # ---- values ------------------------------------------------------

    def chosen_index(self, name):
        """
        Which choice of an option row is currently in force.
        """

        _, choices = OPTION_ROWS[name]

        current = getattr(self.settings, name)

        for index, (_, value) in enumerate(choices):

            if value == current:
                return index

        return 0

    def choose(self, name, index):

        _, choices = OPTION_ROWS[name]

        setattr(self.settings, name, choices[index % len(choices)][1])

    # ---- input -------------------------------------------------------

    def handle_event(self, event):
        """
        Returns "back" when the player leaves the page, else None.
        """

        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.rows)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.rows)

            elif event.key == pygame.K_LEFT:
                self.change(-1)

            elif event.key == pygame.K_RIGHT:
                self.change(1)

            elif event.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER,
                pygame.K_SPACE
            ):
                row = self.rows[self.selected]

                if row == "back":
                    return "back"

                if row == "keyboard":
                    return "instructions"

                self.change(1)

            elif event.key == pygame.K_ESCAPE:
                return "back"

            elif event.key == pygame.K_q:
                return "quit"

        if event.type == pygame.MOUSEMOTION:

            for index, name in enumerate(self.rows):

                if self.row_hovered(name, event.pos):
                    self.selected = index

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.back_rect.collidepoint(event.pos):
                return "back"

            if self.row_hovered("keyboard", event.pos):
                return "instructions"

            for name, rects in self.option_rects.items():

                for index, rect in enumerate(rects):

                    if rect.collidepoint(event.pos):
                        self.choose(name, index)

            for index, rect in enumerate(self.swatch_rects):

                if rect.collidepoint(event.pos):
                    self.settings.color_index = index

        return None

    def row_hovered(self, name, pos):

        if name == "back":
            return self.back_rect.collidepoint(pos)

        return abs(pos[1] - self.row_y[name]) < self.row_spacing // 2

    def change(self, step):
        """
        Change the value of the selected row.
        """

        row = self.rows[self.selected]

        if row == "color":
            self.settings.color_index = (
                self.settings.color_index + step
            ) % len(SNAKE_COLORS)

        elif row in OPTION_ROWS:
            self.choose(row, self.chosen_index(row) + step)

    # ---- drawing -----------------------------------------------------

    def draw(self):

        self.screen.fill(BACKGROUND)

        # Title
        pixelfont.draw(
            self.screen,
            "SETTING",
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

        selected_row = self.rows[self.selected]

        # Labels
        labels = {name: label for name, (label, _) in OPTION_ROWS.items()}
        labels["color"] = "SNAKE COLOR"
        labels["keyboard"] = "KEYBOARD INSTRUCTIONS"

        for name, label in labels.items():

            _, label_height = pixelfont.text_size(label, 3, bold=True)

            pixelfont.draw(
                self.screen,
                label,
                3,
                INK if name == selected_row else DIM,
                topleft=(self.label_x, self.row_y[name] - label_height // 2),
                bold=True
            )

        # Option rows: the chosen box is filled in
        for name, rects in self.option_rects.items():

            _, choices = OPTION_ROWS[name]
            chosen = self.chosen_index(name)

            for index, rect in enumerate(rects):

                if index == chosen:
                    pygame.draw.rect(self.screen, INK, rect)
                    text_color = BACKGROUND
                else:
                    pygame.draw.rect(self.screen, INK, rect, 3)
                    text_color = INK

                pixelfont.draw(
                    self.screen,
                    choices[index][0],
                    2,
                    text_color,
                    center=rect.center,
                    bold=True
                )

        # SNAKE COLOR: swatches
        for index, rect in enumerate(self.swatch_rects):

            pygame.draw.rect(self.screen, SNAKE_COLORS[index][1], rect)

            if index == self.settings.color_index:
                pygame.draw.rect(self.screen, INK, rect.inflate(12, 12), 3)

        # BACK
        if selected_row == "back":
            pygame.draw.rect(self.screen, INK, self.back_rect)
            text_color = BACKGROUND
        else:
            text_color = INK

        pixelfont.draw(
            self.screen,
            "< BACK",
            2,
            text_color,
            center=self.back_rect.center,
            bold=True
        )
