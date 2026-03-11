# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
python -m streamlit run app.py

# Run all tests
pytest

# Run a single test
pytest tests/test_game_logic.py::test_winning_guess
```

## Architecture

This is a CodePath AI110 lab project — a deliberately broken number-guessing game built with Streamlit. The assignment is to find bugs, fix them, and refactor logic out of `app.py`.

**Two-layer structure:**

- `app.py` — Streamlit UI and session state management. All game logic currently lives here as well (this is intentional for the lab; the goal is to move it out).
- `logic_utils.py` — Target module for refactored logic. All four functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) are stubbed with `raise NotImplementedError`. These must be implemented here so that `tests/test_game_logic.py` can import and test them.
- `tests/test_game_logic.py` — Pytest tests that import directly from `logic_utils`. Tests expect `check_guess` to return just the outcome string (e.g. `"Win"`), not the `(outcome, message)` tuple that `app.py` currently uses.

**Key Streamlit state pattern:**
All mutable game state (`secret`, `attempts`, `score`, `status`, `history`) lives in `st.session_state`. Streamlit reruns the entire script on every interaction, so any variable not stored in `st.session_state` resets on each button click.

**Known intentional bugs in `app.py` (part of the lab):**
- `check_guess` (lines 37–40): hint messages are swapped — "Go HIGHER!" fires when guess is too high, "Go LOWER!" fires when guess is too low.
- Lines 158–161: secret is cast to `str` on even-numbered attempts, causing lexicographic comparison instead of numeric.
- `parse_guess`: no range validation; negative numbers and out-of-bound values are accepted.
- Attempts counter initialized to `1` (line 96) but reset to `0` on new game (line 135), causing off-by-one inconsistency.
