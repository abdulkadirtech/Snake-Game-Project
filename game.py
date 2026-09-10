import pygame

from snake import Snake
from food import Food
from ui import UI


class Game:
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
        self.game_over = False

        # Score
        self.score = 0

        # Create Snake
        self.snake = Snake(
            self.width,
            self.height
        )

        # Create Food
        self.food = Food(
            self.width,
            self.height
        )

        # UI
        self.ui = UI(self.screen)

    def run(self):
        """
        Main Game Loop
        """

        while self.running:

            self.handle_events()

            if not self.game_over:
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
                    self.running = False

                # Restart
                if event.key == pygame.K_r:
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

    def draw(self):
        """
        Draw everything
        """

        # Background
        self.screen.fill((25, 25, 30))

        # Draw snake
        self.snake.draw(self.screen)

        # Draw food
        self.food.draw(self.screen)

        # Draw UI
        self.ui.draw_score(self.score)

        # Game Over
        if self.game_over:
            self.ui.draw_game_over(
                self.score
            )

        pygame.display.flip()

    def restart(self):
        """
        Restart game
        """

        self.score = 0
        self.game_over = False

        self.snake = Snake(
            self.width,
            self.height
        )

        self.food = Food(
            self.width,
            self.height
        )