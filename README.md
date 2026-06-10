# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game's purpose:** A simple number-guessing game built with Streamlit. The app picks a
secret number in a range that depends on the chosen difficulty (Easy 1–20, Normal 1–100,
Hard 1–50). You enter guesses and the game tells you whether to go higher or lower until
you find the secret or run out of attempts. A "Developer Debug Info" panel reveals the
secret, score, and history for testing.

**Bugs found:**
- **Inverted hints** — a guess that was too low displayed "Go LOWER!" (and too high showed
  "Go HIGHER!"), pushing the player away from the answer.
- **Secret turned into a string on even attempts** — `app.py` did
  `secret = str(...)` on even attempts, so an integer guess could never equal it (you
  couldn't win) and the comparison ran through a broken text-comparison path.
- **Invalid input wasted an attempt** — the attempt counter was incremented before the
  input was validated, so a blank or non-number guess still burned a turn.
- **Hardcoded range text** — the prompt always said "between 1 and 100" regardless of
  difficulty.
- **"New Game" didn't fully reset** — it left the old score/status/history and drew the
  secret from 1–100 instead of the difficulty's range.

**Fixes applied:**
- Moved all game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`,
  `update_score`) out of `app.py` and into `logic_utils.py` so it can be unit-tested.
- `check_guess` now returns a single outcome string (`"Win"` / `"Too High"` / `"Too Low"`),
  and `app.py` maps that outcome to the **correct** hint direction via a `HINT_MESSAGES` dict.
- Removed the even-attempt string conversion so the secret is always compared as an integer.
- Moved `attempts += 1` inside the valid-guess branch so invalid input no longer costs a turn.
- The range prompt now uses the active difficulty's `low`/`high`, and "New Game" resets
  score, status, history, attempts, and draws a new secret from the correct range.

## 📸 Demo Walkthrough

1. Run `python -m streamlit run app.py` and open the app in your browser.
2. Pick a difficulty in the sidebar (e.g. Normal, 1–100) — the prompt and "Attempts left"
   now match the chosen difficulty.
3. Open **Developer Debug Info** to see the secret number, then enter a guess and click
   **Submit Guess 🚀**.
4. The hint now points the **correct** direction — if your guess is too low it says
   "Go HIGHER!", if too high it says "Go LOWER!" — so you can actually close in on the secret.
5. Try entering a blank space or letters and submit: you get "That is not a number." /
   "Enter a guess." and your attempts left does **not** decrease.
6. Guess the secret to win 🎉 (balloons!), then click **New Game 🔁** to confirm the score,
   history, and attempts fully reset with a fresh secret.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest -v
============================= test session starts ==============================
collected 8 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 12%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 25%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 37%]
tests/test_game_logic.py::test_blank_input_is_rejected PASSED            [ 50%]
tests/test_game_logic.py::test_non_number_is_rejected PASSED             [ 62%]
tests/test_game_logic.py::test_valid_number_is_parsed PASSED             [ 75%]
tests/test_game_logic.py::test_wrong_guess_costs_five_points PASSED      [ 87%]
tests/test_game_logic.py::test_first_attempt_win_awards_full_points PASSED [100%]

============================== 8 passed in 0.03s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
