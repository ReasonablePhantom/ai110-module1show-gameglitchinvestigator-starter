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
| Guesses 50 → 25 → 12 → 18 → 15 → 16 → 17 (secret was 17, Normal difficulty 1–100) | Each hint should point toward 17 — e.g. guess 50 should say "Go LOWER!", guess 12 should say "Go HIGHER!" | Hints were inverted: guess 50 (too high) showed "📈 Go HIGHER!", guess 12 (too low) showed "📉 Go LOWER!" — pushing away from the answer every time | none |
| Correct number guessed on an even-numbered attempt | "🎉 Correct!" / win | Not recognized as a win — the secret was compared as a string, so an int guess never matched | none |
| A blank space `" "` submitted as a guess | Show "That is not a number." and keep my attempts left the same | Showed the error **but still subtracted one attempt** (Attempts left dropped) | none |
| Typed `0` after the out-of-range fix was applied and Streamlit was still running | Show "Enter a number between 1 and 100." with no attempt lost | App crashed with a red error screen | `TypeError: parse_guess() got an unexpected keyword argument 'low'` — Python loaded a stale compiled `.pyc` from `__pycache__` instead of the updated source file. Fixed by deleting `__pycache__` and restarting Streamlit. |

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

Every time you interact with the page (clicking buttons, entering text in input boxes),
Streamlit will re-run the entire script from the beginning. This means that ordinary Python
variables will be recreated every time, so any content you want to "remember" between clicks —
such as secret numbers, scores, and attempts — must be saved in `st.session_state`, as it will
remain unchanged across multiple re-runs. I would explain this to a friend like this: "Imagine
that every time you press a button, the entire program restarts; `session_state` is like that
one notebook that keeps working after the restart. Therefore, any data the game needs to store
should be saved there."

---

## 5. Looking ahead: your developer habits

One habit I wish to maintain is to **write a small automated test for each bug I fix** — this
can transform "I think it will work" into "I can prove it will work", and it can also catch the
bug if it reoccurs. Next time, I will be more skeptical earlier: I hope to first **compare the
AI's diagnostic results with the actual code** before taking any action, because although the
explanation of "secret reset" sounded reasonable, it was actually incorrect. Overall, this
project has made me realize that the code generated by AI may seem perfect and even claim to be
"ready for production", but it actually hides real bugs. Therefore, manual review and testing
are not optional — they are the key to making the AI's output trustworthy.
