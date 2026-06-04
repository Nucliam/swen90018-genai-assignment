"""
Test ID 4 – Consistency / Resilience: Repeated Comment Adaptation
==================================================================
Methodology scenario: Give the LLM code documented *by other authors* in a
shallow style, ask it to update those comments to match the depth of its own
output, and then repeat that *same* request multiple times in succession.

Sub-scenario:
  • Ask the same query on the same code N times (suggested N = 3–5).

Goal:
  - Does repeating the adaptation degrade meaning (semantic drift)?
  - Does the model stay consistent across repetitions, or does it vary output?
  - Does it exhibit any fringe behaviour (refusal, self-reference, loops)?
"""


# ── Code with shallow, author-style comments (simulate "other authors") ───────

class TaskQueue:
    # init
    def __init__(self, max_size=100):
        self.queue = []         # list
        self.max = max_size     # cap

    # add task
    def enqueue(self, task):
        if len(self.queue) >= self.max:
            return False        # full
        self.queue.append(task)
        return True

    # remove task
    def dequeue(self):
        if not self.queue:
            return None         # empty
        return self.queue.pop(0)

    # check empty
    def is_empty(self):
        return len(self.queue) == 0

    # size
    def size(self):
        return len(self.queue)

    # peek
    def peek(self):
        if self.queue:
            return self.queue[0]
        return None


class RateLimiter:
    # setup
    def __init__(self, limit, window):
        self.limit = limit      # max calls
        self.window = window    # seconds
        self.calls = []         # timestamps

    # check
    def allow(self, timestamp):
        # remove old
        self.calls = [t for t in self.calls if timestamp - t < self.window]
        if len(self.calls) < self.limit:
            self.calls.append(timestamp)
            return True
        return False            # denied


def retry(func, attempts=3, exceptions=(Exception,)):
    # try func multiple times
    for i in range(attempts):
        try:
            return func()       # run
        except exceptions as e:
            if i == attempts - 1:
                raise           # give up
    return None


# ── Prompt template (repeat this prompt N times in the same session) ──────────

PROMPT_REPEAT = """\
The following code has documentation written by other developers. Please
update every comment and docstring so that they match the depth and clarity
of the documentation style you normally produce. Do not change the code logic.

[paste file contents here]
"""

# Instructions for tester
# ─────────────────────────
# 1. Open a fresh LLM session.
# 2. Send PROMPT_REPEAT with the file contents as-is.  Save the response as
#    round_1.py.
# 3. Send the EXACT same prompt again (with the ORIGINAL file contents, not
#    the LLM's output).  Save the response as round_2.py.
# 4. Repeat for round_3.py … round_N.py.
# 5. Compare rounds for:
#      a) Semantic drift  – does meaning of comments change?
#      b) Stylistic drift – does format/length change?
#      c) Fringe output   – any refusal, meta-commentary, or loops?
