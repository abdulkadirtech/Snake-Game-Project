"""
Automated checks for the Snake game.

Run from the project folder:
    python test_game.py
"""

import os, sys, random
os.environ["SDL_VIDEODRIVER"] = "dummy"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pygame
pygame.init()
from game import Game
from snake import Snake
from food import Food

ok = True

# ── Test 1: same-frame double key press cannot reverse ──
s = Snake(800, 600)          # starts moving RIGHT
s.change_direction("UP")     # legal
s.change_direction("LEFT")   # must be REJECTED: direction is still RIGHT
s.move()
t1 = s.direction == "UP"
print(f"Test 1 same-frame reverse blocked : {'PASS' if t1 else 'FAIL'} (direction={s.direction})")
ok &= t1

# ── Test 2: first food never spawns on snake ──
bad = 0
for i in range(3000):
    random.seed(i)
    g = Game()
    if g.food.position in g.snake.body:
        bad += 1
t2 = bad == 0
print(f"Test 2 first food off snake (3000): {'PASS' if t2 else 'FAIL'} (collisions={bad})")
ok &= t2

# ── Test 3: restart fully resets state ──
g = Game()
for _ in range(6): g.snake.grow()
g.score = 250
g.game_over = True
g.restart()
t3 = (g.score == 0 and g.game_over is False and len(g.snake.body) == 3
      and g.food.position not in g.snake.body)
print(f"Test 3 restart resets state       : {'PASS' if t3 else 'FAIL'} (len={len(g.snake.body)}, score={g.score})")
ok &= t3

# ── Test 4: collision detection (wall + self) ──
s = Snake(800, 600)
s.body[0] = (-20, 300)
t4a = s.check_collision(800, 600) is True
s = Snake(800, 600)
s.body = [(100,100),(120,100),(100,100)]
t4b = s.check_collision(800, 600) is True
s = Snake(800, 600)
t4c = s.check_collision(800, 600) is False
t4 = t4a and t4b and t4c
print(f"Test 4 collision detection        : {'PASS' if t4 else 'FAIL'}")
ok &= t4

# ── Test 5: eating food grows snake by exactly 1 and scores +10 ──
g = Game()
n0, sc0 = len(g.snake.body), g.score
g.food.position = g.snake.get_head_position()
head = g.snake.get_head_position()
g.food.position = (head[0] + 20, head[1])   # directly ahead (moving RIGHT)
g.update()
t5 = len(g.snake.body) == n0 + 1 and g.score == sc0 + 10
print(f"Test 5 eat -> +1 length, +10 score : {'PASS' if t5 else 'FAIL'} (len {n0}->{len(g.snake.body)}, score {sc0}->{g.score})")
ok &= t5

# ── Test 6: 2000-step random play never crashes ──
try:
    random.seed(42)
    g = Game()
    for _ in range(2000):
        g.snake.change_direction(random.choice(["UP","DOWN","LEFT","RIGHT"]))
        if not g.game_over:
            g.update()
        else:
            g.restart()
    t6 = True
except Exception as e:
    t6 = False
    print("  exception:", e)
print(f"Test 6 2000-step fuzz run          : {'PASS' if t6 else 'FAIL'}")
ok &= t6

pygame.quit()
print()
print("ALL TESTS PASSED" if ok else "SOME TESTS FAILED")
sys.exit(0 if ok else 1)
