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
    if g.foods[0].position in g.snake.body:
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
      and g.foods[0].position not in g.snake.body)
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

# ── Test 5: eating grows snake by 1 and scores per food type ──
def eat(kind, start_score=0, grow=0):
    g = Game()
    g.score = start_score
    g.snake.grow(grow)
    n0 = len(g.snake.body)
    head = g.snake.get_head_position()
    g.foods[0].position = (head[0] + 20, head[1])   # directly ahead (moving RIGHT)
    g.foods[0].kind = kind
    g.update()
    return len(g.snake.body) - n0, g.score

t5 = (eat("apple") == (1, 1)
      and eat("watermelon") == (1, 1)
      and eat("gold") == (3, 3))             # worth 3, so it grows 3
print(f"Test 5 length and score per food   : {'PASS' if t5 else 'FAIL'}")
ok &= t5

# ── Test 5d: eating a bomb explodes and ends the game ──
g = Game()
head = g.snake.get_head_position()
g.foods[0].position = (head[0] + 20, head[1])
g.foods[0].kind = "bomb"
g.update()
t5d = g.game_over and len(g.explosions) == 1
print(f"Test 5d eating a bomb is fatal     : {'PASS' if t5d else 'FAIL'}")
ok &= t5d

# ── Test 5c: a bomb burning out costs nobody anything ──
import food as food_module

def burn_out(cells_away, players=1):
    """Expire a bomb `cells_away` from the player's head."""
    g = Game()
    g.settings.players = players
    g.restart()
    g.snake.grow(9)
    g.score = 12
    if g.rival:
        g.rival.grow(9)
        g.rival_score = 8
    head = g.snake.get_head_position()
    bomb = g.foods[0]
    bomb.kind = "bomb"
    bomb.position = (head[0] + cells_away * 20, head[1])
    bomb.spawned_at = (pygame.time.get_ticks()
                       - food_module.LIFETIMES["bomb"] - 1)
    length = len(g.snake.body)
    g.refresh_food()
    return g, length - len(g.snake.body), 12 - g.score

t5c = True

# it goes off wherever it sits, and neither snake pays for it
for distance in (1, 2, 10):
    g, lost_length, lost_score = burn_out(distance)
    t5c = (t5c and (lost_length, lost_score) == (0, 0)
           and len(g.explosions) == 1
           and not any(f.kind == "bomb" for f in g.foods))

# the same in two-snake mode, right next to the rival too
g, lost_length, lost_score = burn_out(1, players=2)
t5c = (t5c and (lost_length, lost_score) == (0, 0)
       and len(g.rival.body) == 12 and g.rival_score == 8)

g = Game()
g.settings.players = 2
g.restart()
g.rival.grow(9)
g.rival_score = 8
length = len(g.rival.body)
rival_head = g.rival.body[0]
bomb = g.foods[0]
bomb.kind = "bomb"
bomb.position = (rival_head[0] + 20, rival_head[1])
bomb.spawned_at = pygame.time.get_ticks() - food_module.LIFETIMES["bomb"] - 1
g.refresh_food()
t5c = (t5c and len(g.rival.body) == length and g.rival_score == 8
       and g.score == 0)
print(f"Test 5c bomb burnout harms nobody  : {'PASS' if t5c else 'FAIL'}")
ok &= t5c

# ── Test 5f: ordinary food also times out, with no penalty ──
g = Game()
g.snake.grow(6)
g.score = 8
n0 = len(g.snake.body)
g.foods[0].kind = "apple"
g.foods[0].position = (200, 200)
g.foods[0].spawned_at = pygame.time.get_ticks() - food_module.DEFAULT_LIFETIME - 1
t5f = g.foods[0].expired()
g.update()
t5f = (t5f and not g.foods[0].expired()
       and g.score == 8 and len(g.snake.body) == n0 and not g.explosions)
print(f"Test 5f stale food is replaced     : {'PASS' if t5f else 'FAIL'}")
ok &= t5f

# ── Test 5b: food never spawns behind the score bar ──
from theme import HUD_HEIGHT
random.seed(7)
g = Game()
bad = 0
for _ in range(2000):
    g.foods[0].randomize(g.snake.body)
    if g.foods[0].position[1] < HUD_HEIGHT:
        bad += 1
t5b = bad == 0
print(f"Test 5b food below score bar       : {'PASS' if t5b else 'FAIL'} (above={bad})")
ok &= t5b

# ── Test 5e: the snake speeds up with the score, then stops ──
import game as game_module
g = Game()
slow = g.step_interval
g.score = 10
faster = g.step_interval
g.score = 1000
fastest = g.step_interval
t5e = (slow == game_module.START_STEP and faster < slow
       and fastest == game_module.MIN_STEP)
print(f"Test 5e speed rises then caps      : {'PASS' if t5e else 'FAIL'} ({slow}->{faster}->{fastest} ms)")
ok &= t5e

# ── Test 5g: the TIMER setting ends the game when it runs out ──
g = Game()
g.settings.timer = 60
g.restart()
t5g = g.time_left == 60000
g.tick_timer(59999)
t5g = t5g and not g.game_over
g.tick_timer(1)
t5g = t5g and g.game_over and g.time_left == 0
# and with the timer off the clock never ends the game
g.settings.timer = 0
g.restart()
g.tick_timer(10 ** 6)
t5g = t5g and not g.game_over
print(f"Test 5g match timer                : {'PASS' if t5g else 'FAIL'}")
ok &= t5g

# ── Test 5h: PLAYERS MODE builds a second snake ──
g = Game()
g.settings.players = 1
g.restart()
t5h = g.rival is None

g.settings.players = 2
g.restart()
t5h = (t5h and g.rival is not None
       and not (set(g.rival.body) & set(g.snake.body)))

# the rival's colour is re-rolled each game: a random pick of the two
# colours the player is not using
from theme import SNAKE_COLORS
random.seed(1)
names = [entry[0] for entry in SNAKE_COLORS]
for index in range(3):
    g.settings.color_index = index
    seen = set()
    for _ in range(40):
        g.restart()
        t5h = t5h and g.rival.head_color != g.snake.head_color
        seen.add(SNAKE_COLORS[g.settings.rival_index][0])
    t5h = t5h and seen == set(names) - {names[index]}

# the two snakes cannot eat each other: overlapping is harmless
g.restart()
g.rival.body = list(g.snake.body)
g.update()
t5h = t5h and not g.game_over

# the rival feeds itself without scoring for the player
random.seed(3)
g.restart()
fed = False
for _ in range(400):
    if g.game_over:
        g.restart()
    length = len(g.rival.body)
    g.update()
    if len(g.rival.body) > length:
        fed = True
t5h = t5h and fed
print(f"Test 5h two-snake mode             : {'PASS' if t5h else 'FAIL'}")
ok &= t5h

# ── Test 5i: snakes start somewhere different each game ──
random.seed(12)
g = Game()
g.settings.players = 2
pairs = set()
t5i = True
for _ in range(40):
    g.restart()
    pairs.add((g.snake.body[0], g.rival.body[0]))
    # never overlapping, always inside the field
    t5i = t5i and not (set(g.snake.body) & set(g.rival.body))
    for cell in g.snake.body + g.rival.body:
        t5i = t5i and g.field.collidepoint(cell)
t5i = t5i and len(pairs) > 30

# the rival keeps its own tally, which restart clears
g.restart()
g.rival_score = 9
g.restart()
t5i = t5i and g.rival_score == 0
print(f"Test 5i random starts, rival score : {'PASS' if t5i else 'FAIL'} ({len(pairs)}/40 distinct)")
ok &= t5i

# ── Test 5j: fruit and gold call up a successor 2s early ──
def nearly_gone(kind):
    g = Game()
    g.restart()
    food = g.foods[0]
    food.kind = kind
    food.spawned_at = (pygame.time.get_ticks()
                       - food.lifetime + food_module.HANDOVER - 500)
    g.refresh_food()
    return g, food

g, food = nearly_gone("apple")
t5j = len(g.foods) == 2 and g.foods[0].position != g.foods[1].position
g.refresh_food()
t5j = t5j and len(g.foods) == 2          # only ever hands over once

g, _ = nearly_gone("gold")
t5j = t5j and len(g.foods) == 2

# a bomb keeps the field to itself until it goes off
g, _ = nearly_gone("bomb")
t5j = t5j and len(g.foods) == 1

# once the old one times out the field is back to a single food
g, food = nearly_gone("apple")
food.spawned_at = pygame.time.get_ticks() - food.lifetime - 1
g.refresh_food()
t5j = t5j and len(g.foods) == 1 and food not in g.foods
print(f"Test 5j food handed over early     : {'PASS' if t5j else 'FAIL'}")
ok &= t5j

# ── Test 5k: the game-over panel says who won ──
g = Game()
panel = g.gameover_page
t5k = (panel.score_lines(11, None, True) == ["SCORE: 11"]
       and panel.score_lines(9, 6, True) == ["YOU WON", "YOU: 9", "RIVAL: 6"]
       and panel.score_lines(4, 9, True) == ["YOU LOST", "YOU: 4", "RIVAL: 9"]
       # a draw says nothing
       and panel.score_lines(7, 7, True) == ["YOU: 7", "RIVAL: 7"]
       # and pausing mid-game never gives the result away
       and panel.score_lines(9, 6, False) == ["YOU: 9", "RIVAL: 6"])
print(f"Test 5k game-over result line      : {'PASS' if t5k else 'FAIL'}")
ok &= t5k

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
