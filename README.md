# Python Chess Game

A full-featured chess game built with **Python** and **Pygame**, supporting multiple play modes including **local multiplayer**, **LAN multiplayer**, and an **AI opponent**.

---

![Play Against AI](https://i.postimg.cc/Ls5BG4GD/play-Against-AI.png)

## Features

- **Local Multiplayer** — Two players can play on the same computer.
- **LAN Multiplayer** — Host or join games over a local network using a simple server-client model.
- **AI Opponent** — Challenge a chess bot:
  - Initially written in Python.
  - Later ported to a high-performance **C++ DLL** for better efficiency.

---

![Multiplayer](https://i.postimg.cc/sVrkqk6r/Chat-With-Custom-Colors-Show-Case.png)

## AI Details

- The AI evaluates board positions and calculates optimal moves.
- Originally implemented in Python, then optimized using a C++ engine accessed via a dynamically linked library (DLL).
- The Python side communicates with the DLL for fast move generation.

---

### Collaborators

- Special thanks to [Dexxxon09](https://github.com/Dexxxon09) for contributions and support on this project.
