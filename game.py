import pygame

import audio
from snake import Snake
from food import Food
from ui import UI
from menu import Menu
from settings import Settings, SettingsPage
from instructions import InstructionsPage
from panel import PanelPage
from effects import Explosion
from theme import BACKGROUND, INK, CANVAS_WIDTH, CANVAS_HEIGHT, HUD_HEIGHT


# Milliseconds per step: slow to begin with, quicker with every point,
# and never faster than the floor.
START_STEP = 170
MIN_STEP = 80
STEP_PER_POINT = 3


class Game:
    def __init__(self):
        # The window can be resized; everything is drawn straight onto
        # it, so the play field really does get bigger.
        self.screen = pygame.display.set_mode(
            (CANVAS_WIDTH, CANVAS_HEIGHT),
            pygame.RESIZABLE
        )

        self.width = CANVAS_WIDTH
        self.height = CANVAS_HEIGHT

        # Play field, snapped to whole blocks below the score bar.
        self.field = self.field_rect()

        pygame.display.set_caption("Snake Game")

        # Clock
        self.clock = pygame.time.Clock()

        # Game status
        self.running = True
        self.game_over = False

        # "menu", "settings", "instructions" or "playing"
        self.state = "menu"

        self.paused = False

        # The snake steps on a timer, and frames in between are drawn
        # part of the way through the step, so it glides.
        self.step_timer = 0

        # Score
        self.score = 0

        # Player preferences
        self.settings = Settings()

        self.beep = audio.make_beep()
        self.boom = audio.make_explosion()
        self.music = audio.make_music()

        self.music_channel = None

        if self.music:
            self.music.set_volume(0.35)

        # Create Snake
        self.snake = Snake(
            self.field.right,
            self.field.bottom,
            self.settings.head_color,
            self.settings.body_color,
            self.field.top
        )

        # Create Food
        # Pass the snake body so the first food never
        # spawns underneath the snake.
        self.food = self.new_food()

        # UI
        self.ui = UI(self.screen)

        # Pages
        self.menu = Menu(self.screen)
        self.settings_page = SettingsPage(self.screen, self.settings)
        self.instructions_page = InstructionsPage(self.screen)

        self.pause_page = self.build_pause_page()
        self.gameover_page = self.build_gameover_page()

        # Bomb blasts currently playing out
        self.explosions = []

    def build_pause_page(self):

        return PanelPage(
            self.screen,
            "PAUSED",
            "RESUME",
            "resume",
            {
                pygame.K_p: "resume",
                pygame.K_ESCAPE: "resume",
                pygame.K_q: "quit",
            }
        )

    def build_gameover_page(self):

        return PanelPage(
            self.screen,
            "GAME OVER",
            "REPLAY",
            "replay",
            {
                pygame.K_r: "replay",
                pygame.K_ESCAPE: "menu",
                pygame.K_q: "quit",
            }
        )

    @property
    def step_interval(self):
        """
        How long one step takes. The snake speeds up as the score
        climbs, then holds at its fastest.
        """

        return max(MIN_STEP, START_STEP - self.score * STEP_PER_POINT)

    def field_rect(self):
        """
        The play area: everything below the score bar, rounded down to
        whole 20px blocks so the grid always lines up with the edge.
        """

        block = 20

        return pygame.Rect(
            0,
            HUD_HEIGHT,
            max(block * 4, self.width // block * block),
            max(block * 4, (self.height - HUD_HEIGHT) // block * block)
        )

    def new_food(self):

        return Food(
            self.field.right,
            self.field.bottom,
            self.snake.body,
            self.field.top
        )

    def resize(self, size):
        """
        Re-lay out everything for the new window size.
        """

        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)

        self.width, self.height = self.screen.get_size()

        self.field = self.field_rect()

        self.ui = UI(self.screen)

        selected = self.menu.selected
        self.menu = Menu(self.screen)
        self.menu.selected = selected

        selected = self.settings_page.selected
        self.settings_page = SettingsPage(self.screen, self.settings)
        self.settings_page.selected = selected

        self.instructions_page = InstructionsPage(self.screen)

        selected = self.pause_page.selected
        self.pause_page = self.build_pause_page()
        self.pause_page.selected = selected

        selected = self.gameover_page.selected
        self.gameover_page = self.build_gameover_page()
        self.gameover_page.selected = selected

        # Keep the food inside the new field.
        if not self.field.collidepoint(self.food.position):
            self.food = self.new_food()
        else:
            self.food.width = self.field.right
            self.food.height = self.field.bottom
            self.food.top = self.field.top

    def run(self):
        """
        Main Game Loop
        """

        while self.running:

            self.update_music()

            pages = {
                "menu": (self.menu, None),
                "settings": (self.settings_page, "menu"),
                "instructions": (self.instructions_page, "settings"),
            }

            if self.state in pages:

                page, back_state = pages[self.state]

                self.handle_page_events(page, back_state)

                page.draw()
                pygame.display.flip()
                self.clock.tick(30)

            elif self.game_over:
                self.handle_panel_events(self.gameover_page)
                self.draw()
                self.clock.tick(30)

            elif self.paused:
                self.handle_panel_events(self.pause_page)
                self.draw()
                self.clock.tick(30)

            else:
                self.handle_events()

                elapsed = self.clock.tick(60)

                if not self.game_over and not self.paused:

                    self.step_timer += elapsed

                    while (
                        self.step_timer >= self.step_interval
                        and not self.game_over
                    ):

                        self.step_timer -= self.step_interval

                        self.update()

                self.draw()

    def handle_page_events(self, page, back_state=None):
        """
        Feed events to a page and act on the action it returns.
        """

        for event in pygame.event.get():

            if event.type == pygame.VIDEORESIZE:
                self.resize(event.size)
                page = {
                    "menu": self.menu,
                    "settings": self.settings_page,
                    "instructions": self.instructions_page,
                }[self.state]
                continue

            action = page.handle_event(event)

            if action == "start":
                self.restart()
                self.state = "playing"

            elif action == "setting":
                self.state = "settings"

            elif action == "instructions":
                self.state = "instructions"

            elif action == "back" and back_state:
                self.state = back_state

            elif action == "quit":
                self.running = False

    def handle_panel_events(self, panel):
        """
        A panel owns the input while it is up.
        """

        for event in pygame.event.get():

            if event.type == pygame.VIDEORESIZE:
                self.resize(event.size)
                panel = (
                    self.gameover_page if self.game_over else self.pause_page
                )
                continue

            action = panel.handle_event(event)

            if action == "resume":
                self.paused = False

            elif action == "replay":
                self.restart()

            elif action == "menu":
                self.state = "menu"

            elif action == "quit":
                self.running = False

    def handle_events(self):
        """
        Handle keyboard and window events
        """

        for event in pygame.event.get():

            # Close window
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.VIDEORESIZE:
                self.resize(event.size)

            # Keyboard
            if event.type == pygame.KEYDOWN:

                # Back to the home page
                if event.key == pygame.K_ESCAPE:
                    self.state = "menu"

                # Quit the game
                elif event.key == pygame.K_q:
                    self.running = False

                # Open the setting page
                elif event.key == pygame.K_s:
                    self.state = "settings"

                # Pause
                elif event.key == pygame.K_p and not self.game_over:
                    self.paused = not self.paused

                # Restart
                elif event.key == pygame.K_r:
                    self.restart()

                # Snake movement
                if not self.game_over:

                    if event.key == pygame.K_UP:
                        self.snake.change_direction("UP")

                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction("DOWN")

                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction("LEFT")

                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction("RIGHT")

    def update_music(self):
        """
        The background loop runs only while the game is actually being
        played, and only when sound is on.
        """

        if not self.music:
            return

        wanted = (
            self.state == "playing"
            and not self.paused
            and not self.game_over
            and self.settings.sound
        )

        playing = self.music_channel and self.music_channel.get_busy()

        if wanted and not playing:
            self.music_channel = self.music.play(loops=-1)

        elif not wanted and playing:
            self.music_channel.stop()
            self.music_channel = None

    def blow_up(self, position):

        x, y = position

        self.explosions.append(Explosion((x + 10, y + 10)))

        if self.settings.sound and self.boom:
            self.boom.play()

    def update(self):
        """
        Update game objects
        """

        # Move snake
        self.snake.move()

        # Check food
        if self.snake.get_head_position() == self.food.position:

            if self.food.kind == "bomb":

                # Biting a bomb sets it off, and that is the end.
                self.blow_up(self.food.position)

                self.game_over = True

                return

            points = self.food.points

            # The snake's length tracks what it is worth.
            self.snake.grow(points)

            self.score += points

            if self.settings.sound and self.beep:
                self.beep.play()

            self.food.randomize(
                self.snake.body
            )

        # An uneaten bomb goes off, and something else takes its place.
        elif self.food.expired():

            self.blow_up(self.food.position)

            self.food.randomize(
                self.snake.body
            )

        # Check collision
        if self.snake.check_collision(
            self.field.right,
            self.field.bottom,
            self.field.top
        ):
            self.game_over = True

    def draw(self):
        """
        Draw everything
        """

        # Background
        self.screen.fill(BACKGROUND)

        # Draw food
        self.food.draw(self.screen)

        # Draw snake, part way through its current step
        progress = min(1.0, self.step_timer / self.step_interval)

        if self.game_over or self.paused:
            progress = 1.0

        self.snake.draw(self.screen, progress)

        # Bomb blasts
        self.explosions = [
            blast for blast in self.explosions if not blast.finished()
        ]

        for blast in self.explosions:
            blast.draw(self.screen)

        # Play field edge, which grows with the window
        pygame.draw.rect(
            self.screen,
            INK,
            self.field,
            3
        )

        # Draw UI
        self.ui.draw_score(self.score)

        # Game Over
        if self.game_over:
            self.gameover_page.draw(self.score)

        elif self.paused:
            self.pause_page.draw(self.score)

        pygame.display.flip()

    def restart(self):
        """
        Restart game
        """

        self.score = 0
        self.game_over = False
        self.paused = False
        self.step_timer = 0
        self.explosions = []

        self.snake = Snake(
            self.field.right,
            self.field.bottom,
            self.settings.head_color,
            self.settings.body_color,
            self.field.top
        )

        self.food = self.new_food()
