"""
Test ID 2 – Consistency: Partially / Variably Documented Code
==============================================================
Methodology scenario: Give the LLM code that already has *some* documentation,
and observe whether it implicitly matches the existing style or imposes its own.

Four sub-scenarios (prompt separately):
  A) "Expand the documentation" – no style guidance
  B) "Expand the documentation, maintaining the existing style"
  C) After one pass, give radically differently styled code and ask again
  D) "Keep documentation brief and focused on readability"

Goal: Does the model naturally mirror existing style? Does it need prompting?
Does consistency hold across a session?
"""

import os
import json


# ── Already documented – terse, single-line style ────────────────────────────

def load_config(path):
    # open file
    with open(path) as f:
        # parse and return
        return json.load(f)


def save_config(path, data):
    # write json
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ── Partially documented – docstring only, no inline comments ─────────────────

def merge_dicts(base, override):
    """
    Merge two dictionaries, with values from override taking precedence.
    Returns a new dictionary; neither input is mutated.
    """
    result = base.copy()
    for key, value in override.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


# ── Radically different style – verbose, narrative paragraphs ─────────────────

def find_files(directory, extension):
    """
    This function is responsible for traversing the filesystem rooted at the
    provided `directory` argument.  It will walk every subdirectory it
    encounters and, for each file it finds, it will check whether the
    filename ends with the string supplied in `extension`.  All matching
    paths are accumulated into a list which is ultimately returned to the
    caller.  The function does not follow symbolic links and does not raise
    an exception if the directory does not exist – it simply returns an
    empty list in that scenario.
    """
    matches = []
    for root, dirs, files in os.walk(directory):
        for fname in files:
            if fname.endswith(extension):
                matches.append(os.path.join(root, fname))
    return matches


# ── No documentation at all ───────────────────────────────────────────────────

def paginate(items, page_size, page_number):
    start = page_number * page_size
    end = start + page_size
    return items[start:end]


def flatten(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


# ── Prompt templates ──────────────────────────────────────────────────────────

PROMPT_A = """\
Please expand the documentation in the following code.

[paste file contents here]
"""

PROMPT_B = """\
Please expand the documentation in the following code, maintaining the
existing documentation style throughout.

[paste file contents here]
"""

PROMPT_C = """\
Using the same documentation style you applied in our previous exchange,
please document the new functions I've added to the file.

[paste updated file contents here]
"""

PROMPT_D = """\
Please document the following code. Keep comments brief and focused on
readability – one short line per logical block is ideal.

[paste file contents here]
"""
