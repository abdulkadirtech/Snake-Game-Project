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