# Snake Game

A Snake game built with Python and Pygame.

- **Team**: 何岚, 李思齐， 奥马尔
- **Instructor**: 黄天羽
- **Built with**: Python 3, Pygame 2.x

## Running it

```bash
pip install pygame
python main.py
```

The window can be resized, minimised and maximised. The play field grows
with it; the score bar keeps its height.

## Controls

| Key | Action |
|-----|--------|
| ↑ ↓ ← → | Steer the snake (and move around menus) |
| Enter / Space | Choose the selected item |
| P | Pause |
| R | Restart |
| S | Open the setting page (from the home page) |
| Esc | Back to the home page (from a menu, or after game over) |
| Q | Quit (from any menu or panel) |

During play only the arrows, P and R do anything; leaving the game goes
through the pause or game-over panel. Menus and buttons also respond to
the mouse.

## Pages

- **Home** — SNAKE GAME, START, SETTING, QUIT.
- **Setting** — sound on/off, snake colour (green, orange, blue), and a
  link to the instruction page.
- **Instructions** — the key list above.
- **Game** — score bar on top, play field below it.
- **Paused** and **Game Over** — a panel showing the score, with
  RESUME/REPLAY and QUIT.

Everything is drawn in a green-on-black terminal style using a bitmap
font defined in code (`pixelfont.py`), so the game ships with no image
or audio files at all.

## Playing

The snake slithers: a wave travels down its body as it moves, it glides
between cells rather than jumping, and it grows thicker as it gets
longer. It dies on the walls or on itself.

It starts slow and speeds up with every point, from 170 ms per step down
to 80 ms, after which it stays at that pace.

| Food | Effect |
|------|--------|
| Apple, mango, watermelon, kiwi | +1 point, grows 1 segment |
| Gold | +3 points, grows 3 segments |
| Bomb | Eating it explodes and ends the game |

Food does not wait forever. Anything left uneaten blinks and then
vanishes, replaced by something new — fruit after 9 seconds, gold after
6, a bomb after 4. A bomb explodes as it goes: the snake survives the
blast but loses 5 segments and 5 points. So a bomb costs you either way;
it just costs less if you stay away from it.

Sound effects and the background music are generated as waveforms at
startup (`audio.py`). The music only plays during active play, and the
SOUND setting mutes everything.

## Structure

| File | Responsibility |
|------|----------------|
| `main.py` | Entry point: starts Pygame and runs `Game` |
| `game.py` | Main loop, state machine, input, scoring, resizing |
| `snake.py` | Body, movement, collisions, and the slither drawing |
| `food.py` | Food types, spawning, and their artwork |
| `effects.py` | The bomb explosion |
| `menu.py`, `settings.py`, `instructions.py`, `panel.py` | The pages |
| `ui.py` | The score bar |
| `pixelfont.py`, `theme.py` | Bitmap font and shared colours |
| `audio.py` | Generated beep, explosion and music |
| `test_game.py` | Automated checks |

`Game` only coordinates: it never touches the snake's coordinates
directly. Each module owns its own data and drawing.

## Notable details

**No instant reversal.** A direction key sets `next_direction`, which
`move()` commits later, and it is checked against the *committed*
direction. So pressing ↑ then ← in one frame while moving right cannot
turn the snake back into itself.

**Food never hidden.** Spawning resamples until the cell is free of the
snake, and never picks a row behind the score bar.

**Restart rebuilds objects** rather than resetting fields one by one, so
no stale state can survive.

**Fixed-step movement.** The snake steps on a timer while the loop runs
at 60 FPS, and frames in between are drawn part way through the step —
speed is set by that timer, not by how fast the game renders.

## Tests

```bash
python test_game.py
```

Covers reversal blocking, food placement (including staying below the
score bar), restart, collisions, per-food score and growth, the fatal
bomb, bomb burnout, and a 2000-step fuzz run. All passing.
