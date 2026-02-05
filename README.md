# Jeopardy Quiz Game

A Jeopardy-style quiz game built with Python. Play solo or with up to 6 players in buzzer-style mode.

**By Khantushig Batbold**

## Features

- 5 categories: Science, Geography, History, Pop Culture, Technology
- 125 questions (5 per category per point level)
- Multiplayer buzzer-style (no turns — click whoever answered)
- 30-second countdown timer per question
- Time bonus: answer fast for 1.5x points, slow for 0.5x
- Sound effects (correct, wrong, select, victory)
- Persistent leaderboard with score saving
- Gen Z dark theme with purple/green UI

## How to Run

### Streamlit Version (recommended)

```bash
pip install streamlit
streamlit run app.py
```

Opens in your browser at `localhost:8501`.

### CLI Version

```bash
python3 main.py
```

Text-based version with colored output in terminal.

## Game Mechanics

1. Choose number of players (1-6) and enter names
2. Pick a category and point value from the board
3. A question appears with a 30-second countdown timer
4. Click the player who answered correctly (gets points) or wrong (loses points)
5. Time bonus multiplier:
   - Answer within 10s → 1.5x points
   - Answer within 20s → 1.0x points
   - Answer within 30s → 0.5x points
6. Game ends when all questions are answered or you click "End Game"
7. Final standings show winner with scores

## Project Structure

```
quiz_game/
├── app.py           # Streamlit web app (main UI)
├── main.py          # CLI version
├── questions.py     # Question loading and board building
├── scoring.py       # Score saving and leaderboard
├── display.py       # CLI display formatting
├── sounds.py        # Sound effect generation
├── timer.py         # Countdown timer and time bonus
└── data/
    └── questions.json   # 125 questions across 5 categories
```
