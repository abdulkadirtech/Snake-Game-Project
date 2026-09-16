# Snake Game — Flowchart

![Snake Game flowchart](flowchart.png)

Q quits from every menu and panel. Esc means BACK on a menu, RESUME on
PAUSED, and the home page on GAME OVER. During play only the arrow keys,
P (pause) and R (restart) do anything.

The same chart as text, for editing (renders on GitHub and in VS Code):

```mermaid
flowchart TD
    HOME["SNAKE GAME<br/>home page"]
    SET["SETTING<br/>sound, snake colour"]
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
    GAME -- dies --> OVER

    PAUSE -- RESUME --> GAME
    PAUSE -- QUIT --> EXIT

    OVER -- REPLAY --> GAME
    OVER -- QUIT --> EXIT
```
