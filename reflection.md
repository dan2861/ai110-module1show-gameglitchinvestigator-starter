# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

The first time I ran the game it appeared to work on the surface — you could type a number and click Submit — but the feedback was immediately wrong. If I guessed a number lower than the secret, the hint said "Go LOWER!", and if I guessed higher it said "Go HIGHER!", which is the exact opposite of what it should say. The game was also misleading in other ways: decimal inputs like `3.7` were silently truncated to `3` and accepted, and negative numbers or values way above the upper bound went through with no error at all.

Two concrete bugs noticed right away:

1. **Backwards hints** — `check_guess` returned `"Go HIGHER!"` when `guess > secret`, but that means the player already went *too* high and should go lower. The comparison branches were swapped.
2. **No input validation on range or type** — `parse_guess` only checked whether the input could be converted to a number, not whether it fell within the valid range for the chosen difficulty. Negative numbers and values far above the maximum were accepted silently, and decimals were truncated without warning.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used **Cursor (Claude)** as my primary AI tool throughout this project. I described individual bugs in plain language and asked for targeted fixes rather than handing over the whole file at once, which kept the suggestions focused.

- **Correct suggestion:** When I asked about the backwards hint logic, the AI correctly identified that the comparison in `check_guess` had the "Too High" and "Too Low" return values swapped and showed me exactly which two lines to exchange. I verified it by running the app, guessing a number I knew was below the secret, and confirming the hint now read "Go HIGHER!" as expected.
- **Incorrect/misleading suggestion:** When I asked about fixing the score going negative, the AI initially suggested clamping the score to zero at the end of `update_score` with `return max(0, current_score)`. That technically prevented negative numbers, but it masked the real problem — the scoring formula `100 - 10 * (attempt_number + 1)` could produce very low or negative point awards on late guesses, meaning wins were sometimes being punished. I caught this by tracing through the math manually with attempt numbers 8 and 9.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed only when I could reproduce the original bad behavior, apply the fix, and then confirm the correct behavior — not just once, but across a few different inputs. For example, after fixing the hint logic I tested guesses that were too high, too low, and exactly right to make sure all three branches behaved correctly.

One specific test I ran was for `parse_guess`: I manually called it with `"3.7"`, `"-5"`, `"200"`, and `"abc"` in a Python REPL and printed the results. This showed me that while non-numeric strings were rejected, out-of-range and decimal inputs passed through silently — confirming Bug 2 was real and showing me exactly what the function needed to check.

The AI helped me think through edge cases for testing. When I described what `parse_guess` was supposed to do, it suggested I also test the empty string and `None` inputs (which were already handled), but more usefully reminded me that integer conversion of a float string like `"3.7"` would not raise an exception — it would just silently truncate — which is why the original `FIXME` branch was buggy by design.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number kept changing because Streamlit re-runs the entire Python script from top to bottom every time the user interacts with the page — clicking a button, typing in a box, anything. Without session state, the line `random.randint(low, high)` was being called fresh on every single rerun, picking a new secret each time and making the game impossible.

Streamlit "reruns" means that your script is not like a normal program that runs once and waits. It runs again from scratch every time something on the page changes — think of it like refreshing a webpage. `st.session_state` is a dictionary that persists across those reruns, so values you store there survive the re-execution. I'd explain it to a friend like this: *imagine your code is a whiteboard that gets erased and redrawn every time someone clicks a button. Session state is a sticky note you tape to the wall before the board gets erased — it's still there after.*

The fix that gave the game a stable secret was wrapping the `random.randint` call in an `if "secret" not in st.session_state:` guard. This means the secret is only generated once — the first time the app loads — and every subsequent rerun finds the key already in session state and skips over it.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to carry forward is **testing edge cases before assuming a function works**. I used to run the happy path (a normal valid input), see it pass, and move on. This project showed me that the most revealing tests are the weird ones — negative numbers, decimals, empty strings — because that is where the real bugs hide. I plan to always write at least two or three edge-case inputs for any function I either write or receive from AI.

Next time I work with AI on a coding task I would be more deliberate about **asking "why" before accepting a fix**. A few times I took a suggested change, saw it pass my quick test, and moved on — only to discover it was a surface fix that hid a deeper issue. Asking the AI to explain *why* the change works would help me catch those cases faster.

This project made me realize that AI-generated code needs to be treated like code from a new teammate who is very fast but not always careful — it can produce something that looks right and even runs without errors, but the logic may still be subtly wrong in ways that only show up under specific conditions.
