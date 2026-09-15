import pygame


class UI:
    def __init__(self, screen):

        self.screen = screen

        self.font = pygame.font.Font(
            None,
            32
        )

        self.large_font = pygame.font.Font(
            None,
            60
        )

        self.button_font = pygame.font.Font(
            None,
            28
        )

        self.home_buttons = {
            "START": pygame.Rect(300, 220, 200, 60),
            "SETTINGS": pygame.Rect(300, 300, 200, 60),
            "QUIT": pygame.Rect(300, 380, 200, 60),
        }

        self.color_palette = [
            (80, 220, 100),
            (255, 165, 0),
            (70, 130, 220),
            (220, 60, 60),
            (180, 120, 255),
        ]

        self.settings_buttons = {
            "SOUND": pygame.Rect(240, 180, 320, 50),
            "KEYBOARD": pygame.Rect(240, 420, 320, 55),
            "BACK": pygame.Rect(240, 490, 320, 55),
        }

        self.color_rects = [
            pygame.Rect(150 + index * 110, 285, 55, 55)
            for index in range(len(self.color_palette))
        ]

    def draw_score(self, score):

        text = self.font.render(
            f"Score: {score}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            text,
            (20, 20)
        )

    def draw_button(self, rect, label, fill_color, border_color=(255, 255, 255)):
        pygame.draw.rect(
            self.screen,
            fill_color,
            rect,
            border_radius=15
        )

        pygame.draw.rect(
            self.screen,
            border_color,
            rect,
            width=3,
            border_radius=15
        )

        text = self.button_font.render(
            label,
            True,
            (255, 255, 255)
        )
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

    def draw_home_screen(self):
        title = self.large_font.render(
            "SNAKE",
            True,
            (255, 255, 255)
        )
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 120))
        self.screen.blit(title, title_rect)

        self.draw_button(
            self.home_buttons["START"],
            "START",
            (72, 152, 84)
        )
        self.draw_button(
            self.home_buttons["SETTINGS"],
            "SETTINGS",
            (61, 104, 168)
        )
        self.draw_button(
            self.home_buttons["QUIT"],
            "QUIT",
            (166, 58, 58)
        )

    def get_home_button_for_point(self, point):
        for name, rect in self.home_buttons.items():
            if rect.collidepoint(point):
                return name
        return None

    def draw_settings_screen(self, sound_on=True, snake_color=(80, 220, 100)):
        title = self.large_font.render(
            "SETTINGS",
            True,
            (255, 255, 255)
        )
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 110))
        self.screen.blit(title, title_rect)

        sound_label = "SOUND: ON" if sound_on else "SOUND: OFF"
        sound_text = self.font.render(sound_label, True, (255, 255, 255))
        sound_rect = sound_text.get_rect(center=(self.screen.get_width() // 2, 180))
        self.screen.blit(sound_text, sound_rect)

        color_label = self.font.render("SNAKE COLOR", True, (220, 220, 220))
        color_label_rect = color_label.get_rect(center=(self.screen.get_width() // 2, 250))
        self.screen.blit(color_label, color_label_rect)

        for index, color in enumerate(self.color_palette):
            rect = self.color_rects[index]
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(
                self.screen,
                (255, 255, 255) if color == snake_color else (100, 100, 100),
                rect,
                width=4,
                border_radius=10
            )

        self.draw_button(
            self.settings_buttons["KEYBOARD"],
            "KEYBOARD INSTRUCTIONS",
            (61, 104, 168)
        )

        self.draw_button(
            self.settings_buttons["BACK"],
            "BACK",
            (166, 58, 58)
        )

        self.draw_button(
            self.settings_buttons["SOUND"],
            sound_label,
            (72, 152, 84) if sound_on else (110, 110, 110)
        )

    def get_settings_button_for_point(self, point):
        for name, rect in self.settings_buttons.items():
            if rect.collidepoint(point):
                return name
        return None

    def get_color_for_point(self, point):
        for rect, color in zip(self.color_rects, self.color_palette):
            if rect.collidepoint(point):
                return color
        return None

    def draw_key_box(self, x, y, label, width=60, height=40):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (60, 90, 150), rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, width=2, border_radius=8)
        text = self.font.render(label, True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)
        return rect

    def draw_instructions_screen(self):
        title = self.large_font.render(
            "KEYBOARD",
            True,
            (255, 255, 255)
        )
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 90))
        self.screen.blit(title, title_rect)

        action_rows = [
            ("↑ ↓ ← →", "Move", 150, 170),
            ("P", "Pause / Resume", 150, 240),
            ("R", "Restart", 150, 310),
            ("Q", "Quit to Home", 150, 380),
        ]

        for key_label, action_label, x, y in action_rows:
            self.draw_key_box(x, y, key_label)
            label_text = self.font.render(action_label, True, (230, 230, 230))
            text_rect = label_text.get_rect(midleft=(x + 90, y + 20))
            self.screen.blit(label_text, text_rect)

        self.draw_button(
            pygame.Rect(240, 470, 320, 50),
            "BACK",
            (166, 58, 58)
        )

        back_hint = self.font.render("BACK -> SETTINGS", True, (200, 200, 200))
        back_hint_rect = back_hint.get_rect(center=(self.screen.get_width() // 2, 540))
        self.screen.blit(back_hint, back_hint_rect)

    def get_instructions_back_rect(self):
        return pygame.Rect(240, 470, 320, 50)

    def draw_paused_screen(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        title = self.large_font.render(
            "PAUSED",
            True,
            (255, 255, 255)
        )
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 250))
        self.screen.blit(title, title_rect)

        hint = self.font.render(
            "Press Enter or Space to Resume",
            True,
            (255, 255, 255)
        )
        hint_rect = hint.get_rect(center=(self.screen.get_width() // 2, 330))
        self.screen.blit(hint, hint_rect)

    def draw_game_over(self, score):

        # Dark overlay
        overlay = pygame.Surface(
            self.screen.get_size()
        )

        overlay.set_alpha(180)

        overlay.fill(
            (0, 0, 0)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        # Game Over
        title = self.large_font.render(
            "GAME OVER",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(
                self.screen.get_width() // 2,
                250
            )
        )

        self.screen.blit(
            title,
            title_rect
        )

        # Score
        score_text = self.font.render(
            f"Score: {score}",
            True,
            (255, 255, 255)
        )

        score_rect = score_text.get_rect(
            center=(
                self.screen.get_width() // 2,
                320
            )
        )

        self.screen.blit(
            score_text,
            score_rect
        )

        # Restart instruction
        restart_text = self.font.render(
            "Press R to Restart",
            True,
            (255, 255, 255)
        )

        restart_rect = restart_text.get_rect(
            center=(
                self.screen.get_width() // 2,
                380
            )
        )

        self.screen.blit(
            restart_text,
            restart_rect
        )