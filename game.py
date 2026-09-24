import random

import pygame

import ai
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

        # Milliseconds left when the TIMER setting is on.
        self.time_left = 0

        # Score
        self.score = 0

        # Player preferences
        self.settings = Settings()

        # The second snake, when PLAYERS MODE is 2
        self.rival = None
        self.rival_score = 0

        # Everything edible on the field right now
        self.foods = []

        self.beep = audio.make_beep()
        self.boom = audio.make_explosion()
        self.music = audio.make_music()

        self.music_channel = None

        if self.music:
            self.music.set_volume(0.35)

        if self.beep:
            self.beep.set_volume(0.35)

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
        self.foods = [self.new_food()]

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

    def occupied(self):
        """
        Every cell a snake is sitting on.
        """

        cells = list(self.snake.body)

        if self.rival:
            cells += self.rival.body

        cells += [food.position for food in self.foods]

        return cells

    def new_food(self):

        return Food(
            self.field.right,
            self.field.bottom,
            self.occupied(),
            self.field.top
        )

    def random_start(self, avoid=()):
        """
        A block-aligned starting cell with room for the snake's tail,
        well clear of anything in `avoid`.
        """

        block = 20

        columns = self.field.width // block
        rows = self.field.height // block

        avoid = set(avoid)

        for _ in range(200):

            x = self.field.left + random.randrange(3, max(4, columns - 1)) * block
            y = self.field.top + random.randrange(0, rows) * block

            body = [(x - index * block, y) for index in range(3)]

            # Keep a few cells between the two snakes.
            clash = any(
                abs(cell[0] - other[0]) + abs(cell[1] - other[1]) < 4 * block
                for cell in body
                for other in avoid
            )

            if not clash:
                return (x, y)

        return (self.field.centerx // block * block,
                self.field.centery // block * block)

    def new_rival(self, avoid=()):
        """
        The second snake, started somewhere clear of the player's.
        """

        start = self.random_start(avoid)

        return Snake(
            self.field.right,
            self.field.bottom,
            self.settings.rival_head_color,
            self.settings.rival_body_color,
            self.field.top,
            start
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

        # Keep every food inside the new field.
        for index, food in enumerate(self.foods):

            if not self.field.collidepoint(food.position):
                self.foods[index] = self.new_food()
            else:
                food.width = self.field.right
                food.height = self.field.bottom
                food.top = self.field.top

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

                    self.tick_timer(elapsed)

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

                # Only pause and restart work mid-game; everything
                # else goes through the pause or game-over panel.
                if event.key == pygame.K_p and not self.game_over:
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

    def tick_timer(self, elapsed):
        """
        Run the match clock down, and end the game when it empties.
        """

        if not self.settings.timer:
            return

        self.time_left = max(0, self.time_left - elapsed)

        if self.time_left == 0:
            self.game_over = True

    def blow_up(self, position):

        x, y = position

        self.explosions.append(Explosion((x + 10, y + 10)))

        if self.settings.sound and self.boom:
            self.boom.play()

    def food_at(self, cell):
        """
        Take the food sitting on `cell`, if any, off the field.
        """

        for food in self.foods:

            if food.position == cell:
                self.foods.remove(food)
                return food

        return None

    def nearest_safe_food(self):
        """
        Where the rival should head: the closest food that is not a
        bomb.
        """

        head_x, head_y = self.rival.body[0]

        edible = [food for food in self.foods if food.kind != "bomb"]

        if not edible:
            return None

        return min(
            (food.position for food in edible),
            key=lambda pos: abs(pos[0] - head_x) + abs(pos[1] - head_y)
        )

    def refresh_food(self):
        """
        Clear out anything that has run out of time, let fruit and gold
        call up their replacement early, and never leave the field
        empty.
        """

        for food in list(self.foods):

            if food.expired():

                # A bomb goes off as it goes, but the blast is for
                # show: it costs neither snake anything.
                if food.kind == "bomb":

                    self.blow_up(food.position)

                self.foods.remove(food)

            elif food.wants_successor():

                food.handed_over = True

                self.foods.append(self.new_food())

        if not self.foods:
            self.foods.append(self.new_food())

    def update(self):
        """
        Update game objects
        """

        # Move snake
        self.snake.move()

        # Check food
        eaten = self.food_at(self.snake.get_head_position())

        if eaten:

            if eaten.kind == "bomb":

                # Biting a bomb sets it off, and that is the end.
                self.blow_up(eaten.position)

                self.game_over = True

                return

            points = eaten.points

            # The snake's length tracks what it is worth.
            self.snake.grow(points)

            self.score += points

            if self.settings.sound and self.beep:
                self.beep.play()

        self.refresh_food()

        # Check collision
        if self.snake.check_collision(
            self.field.right,
            self.field.bottom,
            self.field.top
        ):
            self.game_over = True

        self.update_rival()

    def update_rival(self):
        """
        Move the second snake. It plays for itself: it scores nothing,
        and the two snakes pass through each other.
        """

        if not self.rival:
            return

        # It leaves bombs well alone.
        target = self.nearest_safe_food()

        # Bombs are cells to stay out of, not just targets to ignore.
        bombs = [
            food.position for food in self.foods if food.kind == "bomb"
        ]

        self.rival.change_direction(
            ai.next_direction(
                self.rival,
                target,
                self.field,
                self.snake.body,
                bombs
            )
        )

        self.rival.move()

        eaten = self.food_at(self.rival.get_head_position())

        if eaten:

            if eaten.kind == "bomb":
                self.blow_up(eaten.position)
                self.rival = self.new_rival(self.snake.body)
            else:
                self.rival.grow(eaten.points)
                self.rival_score += eaten.points

            self.refresh_food()

        # Walls and its own body still finish it, and it starts over.
        if self.rival.check_collision(
            self.field.right,
            self.field.bottom,
            self.field.top
        ):
            self.rival = self.new_rival(self.snake.body)

    def draw(self):
        """
        Draw everything
        """

        # Background
        self.screen.fill(BACKGROUND)

        # Draw food
        for food in self.foods:
            food.draw(self.screen)

        # Draw snake, part way through its current step
        progress = min(1.0, self.step_timer / self.step_interval)

        if self.game_over or self.paused:
            progress = 1.0

        if self.rival:
            self.rival.draw(self.screen, progress)

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
        self.ui.draw_score(
            self.score,
            self.time_left if self.settings.timer else None,
            self.rival_score if self.rival else None
        )

        # Game Over
        if self.game_over:
            self.gameover_page.draw(
                self.score,
                self.rival_score if self.rival else None,
                show_result=True
            )

        elif self.paused:
            self.pause_page.draw(self.score, self.rival_score if self.rival else None)

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
        self.time_left = self.settings.timer * 1000

        self.snake = Snake(
            self.field.right,
            self.field.bottom,
            self.settings.head_color,
            self.settings.body_color,
            self.field.top,
            self.random_start()
        )

        self.rival_score = 0

        if self.settings.players == 2:
            self.settings.pick_rival_color()
            self.rival = self.new_rival(self.snake.body)
        else:
            self.rival = None

        self.foods = [self.new_food()]
