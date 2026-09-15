import pygame

from snake import Snake
from food import Food
from ui import UI


class Game:
    SCREEN_STATES = (
        "HOME",
        "SETTINGS",
        "INSTRUCTIONS",
        "PLAYING",
        "PAUSED",
        "GAME_OVER",
    )

    def __init__(self):
        # Window
        self.width = 800
        self.height = 600

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("Snake Game")

        # Clock
        self.clock = pygame.time.Clock()

        # Game status
        self.running = True
        self.state = "HOME"
        self.game_over = False

        # Settings
        self.settings = {
            "sound_on": True,
            "snake_color": (80, 220, 100),
        }

        # Score
        self.score = 0

        # Create Snake
        self.snake = Snake(
            self.width,
            self.height,
            self.settings["snake_color"]
        )

        # Create Food
        # Pass the snake body so the first food never
        # spawns underneath the snake.
        self.food = Food(
            self.width,
            self.height,
            self.snake.body
        )

        # UI
        self.ui = UI(self.screen)

    def switch_screen(self, new_state):
        """Switch to a valid game screen state."""

        normalized = str(new_state).upper()

        if normalized not in self.SCREEN_STATES:
            raise ValueError(f"Unknown screen state: {new_state}")

        self.state = normalized

        if normalized == "PLAYING":
            self.game_over = False

    def start_game(self):
        """Reset the board and enter gameplay."""

        self.restart()
        self.switch_screen("PLAYING")

    def pause_game(self):
        if self.state == "PLAYING":
            self.switch_screen("PAUSED")

    def resume_game(self):
        if self.state == "PAUSED":
            self.switch_screen("PLAYING")

    def run(self):
        """
        Main Game Loop
        """

        while self.running:

            self.handle_events()

            if self.state == "PLAYING" and not self.game_over:
                self.update()

            self.draw()

            self.clock.tick(10)

    def handle_events(self):
        """
        Handle keyboard and window events
        """

        for event in pygame.event.get():

            # Close window
            if event.type == pygame.QUIT:
                self.running = False

            # Keyboard
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    if self.state == "PLAYING":
                        self.pause_game()
                    elif self.state == "PAUSED":
                        self.resume_game()
                    else:
                        self.running = False

                if event.key == pygame.K_p:
                    if self.state == "PLAYING":
                        self.pause_game()
                    elif self.state == "PAUSED":
                        self.resume_game()

                if event.key == pygame.K_q:
                    if self.state in ("PLAYING", "PAUSED", "GAME_OVER"):
                        self.switch_screen("HOME")

                # Screen navigation
                if self.state == "HOME":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.start_game()
                    elif event.key == pygame.K_s:
                        self.switch_screen("SETTINGS")
                    elif event.key == pygame.K_i:
                        self.switch_screen("INSTRUCTIONS")

                elif self.state == "SETTINGS":
                    if event.key == pygame.K_ESCAPE:
                        self.switch_screen("HOME")
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.switch_screen("HOME")

                elif self.state == "INSTRUCTIONS":
                    if event.key == pygame.K_ESCAPE:
                        self.switch_screen("SETTINGS")
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.switch_screen("SETTINGS")

                elif self.state == "PAUSED":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.resume_game()
                    elif event.key == pygame.K_r:
                        self.start_game()

                elif self.state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.switch_screen("HOME")

                # Snake movement
                if self.state == "PLAYING" and not self.game_over:

                    if event.key == pygame.K_UP:
                        self.snake.change_direction("UP")

                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction("DOWN")

                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction("LEFT")

                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction("RIGHT")

            # Mouse button handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "HOME":
                    self.handle_home_click(event.pos)
                elif self.state == "SETTINGS":
                    self.handle_settings_click(event.pos)
                elif self.state == "INSTRUCTIONS":
                    if self.ui.get_instructions_back_rect().collidepoint(event.pos):
                        self.switch_screen("SETTINGS")

    def handle_home_click(self, point):
        """Handle mouse clicks on the home screen buttons."""

        button_name = self.ui.get_home_button_for_point(point)

        if button_name == "START":
            self.start_game()
        elif button_name == "SETTINGS":
            self.switch_screen("SETTINGS")
        elif button_name == "QUIT":
            self.running = False

    def handle_settings_click(self, point):
        """Handle mouse clicks on the settings screen."""

        sound_toggle = self.ui.get_settings_button_for_point(point)

        if sound_toggle == "SOUND":
            self.settings["sound_on"] = not self.settings["sound_on"]
            return

        if sound_toggle == "KEYBOARD":
            self.switch_screen("INSTRUCTIONS")
            return

        if sound_toggle == "BACK":
            self.switch_screen("HOME")
            return

        color = self.ui.get_color_for_point(point)
        if color is not None:
            self.settings["snake_color"] = color
            self.snake.color = color

    def update(self):
        """
        Update game objects
        """

        # Move snake
        self.snake.move()

        # Check food
        if self.snake.get_head_position() == self.food.position:

            self.snake.grow()

            self.score += 10

            self.food.randomize(
                self.snake.body
            )

        # Check collision
        if self.snake.check_collision(
            self.width,
            self.height
        ):
            self.game_over = True
            self.switch_screen("GAME_OVER")

    def draw(self):
        """
        Draw everything
        """

        # Background
        self.screen.fill((25, 25, 30))

        if self.state == "HOME":
            self.ui.draw_home_screen()
            pygame.display.flip()
            return

        if self.state == "SETTINGS":
            self.ui.draw_settings_screen(
                self.settings["sound_on"],
                self.settings["snake_color"]
            )
            pygame.display.flip()
            return

        if self.state == "INSTRUCTIONS":
            self.ui.draw_instructions_screen()
            pygame.display.flip()
            return

        if self.state == "PAUSED":
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.ui.draw_score(self.score)
            self.ui.draw_paused_screen()
            pygame.display.flip()
            return

        if self.state == "GAME_OVER":
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.ui.draw_score(self.score)
            self.ui.draw_game_over(self.score)
            pygame.display.flip()
            return

        # Default: playing screen
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.ui.draw_score(self.score)

        pygame.display.flip()

    def restart(self):
        """
        Restart game
        """

        self.score = 0
        self.game_over = False
        self.state = "PLAYING"

        self.snake = Snake(
            self.width,
            self.height,
            self.settings["snake_color"]
        )

        self.food = Food(
            self.width,
            self.height,
            self.snake.body
        )