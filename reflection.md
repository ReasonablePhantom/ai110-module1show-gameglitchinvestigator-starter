# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran the game it looked normal, but it was unplayable. I played a couple of
rounds and the hints never made sense — no matter what I guessed it kept telling me to
"Go LOWER!", so I kept guessing smaller numbers (50 → 25 → 15 → 1) and moved further away
from the answer instead of closing in. It felt impossible to win. Two clear bugs stood out
right away: **(1) the hints were backwards**, and **(2) invalid input (a blank space) still
used up one of my attempts.** Looking at the Developer Debug Info panel and the history also
showed strange repeated values, which pointed to a third bug where the secret was being
handled inconsistently between turns.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guesses 50, 25, 15, 1 (secret was higher, e.g. 98) | When the guess is too low, the hint should say "Go HIGHER!" | Hint always said "📉 Go LOWER!", pushing me away from the answer | none |
| Correct number guessed on an even-numbered attempt | "🎉 Correct!" / win | Not recognized as a win — the secret was compared as a string, so an int guess never matched | none |
| A blank space `" "` submitted as a guess | Show "That is not a number." and keep my attempts left the same | Showed the error **but still subtracted one attempt** (Attempts left dropped) | none |
| Typed `0` after the out-of-range fix was applied and Streamlit was still running | Show "Enter a number between 1 and 100." with no attempt lost | App crashed with a red error screen | `TypeError: parse_guess() got an unexpected keyword argument 'low'` — Python loaded a stale compiled `.pyc` from `__pycache__` instead of the updated source file. Fixed by deleting `__pycache__` and restarting Streamlit. |

<!-- EDIT: swap in the exact numbers/secret you actually saw while playing if they differ. -->

---

## 2. How did you use AI as a teammate?

I used my AI coding assistant (Claude Code inside VS Code) to explain the buggy logic,
plan the refactor, and generate tests.

**A correct suggestion:** I asked the AI why the game always said "Go LOWER!" and it walked
through `check_guess` line by line, pointing out that the outcome `"Too Low"` was paired with
the message `"Go LOWER!"` — the messages were attached to the wrong outcomes. I verified this
by reading the function myself and by playing again: every time my guess was below the secret
it said "Go LOWER", which is exactly backwards. After the fix I confirmed in the live game
that a too-low guess now says "Go HIGHER!".

**An incorrect/misleading suggestion:** The project's framing (and a quick AI prompt about a
"State Bug") pointed me toward the idea that *the secret number resets every time you click
Submit* — a classic Streamlit `session_state` problem. When I actually inspected the code and
watched the Debug Info panel, the secret stayed the same across submits; it was correctly
stored in `session_state`. The real bug was different: on **even** attempts the code did
`secret = str(secret)`, so the comparison broke. I verified by reading `app.py` and noticing
the `str()` conversion, not by trusting the "state reset" explanation.

<!-- EDIT: if you actually used ChatGPT/Copilot/Gemini too, mention which and where. -->

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed when I could both (a) see correct behavior in the live game
and (b) prove it with an automated test. For example, after fixing the hints I ran
`python -m pytest -v` and watched `test_guess_too_high` and `test_guess_too_low` pass, which
showed `check_guess(60, 50)` returns `"Too High"` and `check_guess(40, 50)` returns `"Too Low"`.
For the invalid-input bug I added `test_blank_input_is_rejected`, which confirmed
`parse_guess(" ")` returns `ok = False` so the app can skip counting it as an attempt. In the
end all **26 tests passed**. The AI helped me design the new tests by suggesting small,
single-purpose cases (one assertion each), and I reviewed every one to make sure it actually
matched the behavior I wanted rather than just passing.

---

## 4. What did you learn about Streamlit and state?

Streamlit re-runs your entire script from top to bottom every time you interact with the page
(click a button, type in a box). That means normal Python variables are recreated each run, so
anything you want to *remember* between clicks — like the secret number, score, and attempts —
has to live in `st.session_state`, which persists across reruns. I'd explain it to a friend
like this: "Imagine the whole program restarts every time you press a button; `session_state`
is the one notebook that survives the restart, so that's where you keep anything the game needs
to remember."

---

## 5. Looking ahead: your developer habits

One habit I want to keep is **writing a small automated test for every bug I fix** — it turns
"I think it works" into "I can prove it works," and it catches the bug if it ever comes back.
Next time I'd be more skeptical earlier: I want to **verify an AI's diagnosis against the
actual code before acting on it**, since the "secret resets" explanation sounded convincing but
was wrong. Overall this project showed me that AI-generated code can look polished and even
claim to be "production-ready" while hiding real bugs, so human review and tests aren't
optional — they're the part that makes the AI's output trustworthy.

<!-- EDIT: make sections 4 and 5 sound like you — add your own wording or an example. -->
