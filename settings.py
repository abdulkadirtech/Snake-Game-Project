import pygame

import pixelfont
from theme import BACKGROUND, INK, DIM, SNAKE_COLORS


class Settings:
    """
    Player preferences, shared between the pages and the game.
    """

    def __init__(self):

        self.sound = True
        self.color_index = 0

    @property
    def head_color(self):
        return SNAKE_COLORS[self.color_index][1]

    @property
    def body_color(self):
        return SNAKE_COLORS[self.color_index][2]


class SettingsPage:
    """
    The setting page: sound, snake colour, keyboard instructions, back.
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

        self.rows = ["sound", "color", "keyboard", "back"]

        self.row_y = {
            "sound": 235,
            "color": 305,
            "keyboard": 375,
        }

        # ON / OFF boxes
        on_width, on_height = pixelfont.text_size("ON", 2, bold=True)
        off_width, _ = pixelfont.text_size("OFF", 2, bold=True)

        box_height = on_height + 14

        self.on_rect = pygame.Rect(
            self.value_x,
            self.row_y["sound"] - box_height // 2,
            on_width + 20,
            box_height
        )

        self.off_rect = pygame.Rect(
            self.on_rect.right + 6,
            self.on_rect.top,
            off_width + 20,
            box_height
        )

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
            height - 120,
            back_width + 20,
            back_height + 14
        )

        self.selected = 0

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

        if event.type == pygame.MOUSEMOTION:

            for index, name in enumerate(self.rows):

                if self.row_hovered(name, event.pos):
                    self.selected = index

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.back_rect.collidepoint(event.pos):
                return "back"

            if self.row_hovered("keyboard", event.pos):
                return "instructions"

            if self.on_rect.collidepoint(event.pos):
                self.settings.sound = True

            elif self.off_rect.collidepoint(event.pos):
                self.settings.sound = False

            for index, rect in enumerate(self.swatch_rects):

                if rect.collidepoint(event.pos):
                    self.settings.color_index = index

        return None

    def row_hovered(self, name, pos):

        if name == "back":
            return self.back_rect.collidepoint(pos)

        return abs(pos[1] - self.row_y[name]) < 30

    def change(self, step):
        """
        Change the value of the selected row.
        """

        row = self.rows[self.selected]

        if row == "sound":
            self.settings.sound = not self.settings.sound

        elif row == "color":
            self.settings.color_index = (
                self.settings.color_index + step
            ) % len(SNAKE_COLORS)

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
        for name, label in (
            ("sound", "SOUND"),
            ("color", "SNAKE COLOR"),
            ("keyboard", "KEYBOARD INSTRUCTIONS"),
        ):
            _, label_height = pixelfont.text_size(label, 3, bold=True)

            pixelfont.draw(
                self.screen,
                label,
                3,
                INK if name == selected_row else DIM,
                topleft=(self.label_x, self.row_y[name] - label_height // 2),
                bold=True
            )

        # SOUND: ON / OFF
        for rect, label, active in (
            (self.on_rect, "ON", self.settings.sound),
            (self.off_rect, "OFF", not self.settings.sound),
        ):
            if active:
                pygame.draw.rect(self.screen, INK, rect)
                text_color = BACKGROUND
            else:
                pygame.draw.rect(self.screen, INK, rect, 3)
                text_color = INK

            pixelfont.draw(
                self.screen,
                label,
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
