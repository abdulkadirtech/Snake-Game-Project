# Snake Game — Flowchart

![Snake Game flowchart](flowchart.png)

Q quits from every menu and panel. Esc means BACK on a menu, RESUME on
PAUSED, and the home page on GAME OVER. During play only the arrow keys,
P (pause) and R (restart) do anything.

GAME OVER comes from hitting a wall, biting yourself, eating a bomb, or
the timer running out. Its panel shows the final score — both scores in
two-snake mode, headed by YOU WON or YOU LOST.

The same chart as text, for editing (renders on GitHub and in VS Code):

```mermaid
flowchart TD
    HOME["SNAKE GAME<br/>home page"]
    SET["SETTING<br/>sound, colour, players, timer"]
    INS["INSTRUCTIONS"]
    GAME["GAME<br/>playing"]
    PAUSE["PAUSED"]
    OVER["GAME OVER"]
    EXIT(("EXIT"))

    HOME -- START --> GAME
    HOME -- SETTING --> SET
    HOME -- QUIT --> EXIT

    SET -- KEYBOARD INSTRUCTIONS --> INS
    SET -- BACK --> HOME
    INS -- BACK --> SET

    GAME -- P --> PAUSE
    GAME -- R restart --> GAME
    GAME -- "dies / time up" --> OVER

    PAUSE -- RESUME --> GAME
    PAUSE -- QUIT --> EXIT

    OVER -- REPLAY --> GAME
    OVER -- QUIT --> EXIT
```

Both pictures are drawn by `draw_flowchart.py` and `draw_structure.py`
in this folder:

```bash
python docs/draw_flowchart.py
python docs/draw_structure.py
```
