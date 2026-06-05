# SWEN90018 – Gen AI Methodology Test Suite
## Code Documentation Study

This folder contains the test code for the four methodology scenarios described
in the assignment report.  Each file is self-contained and includes embedded
prompt templates at the bottom.

---

### Files

| File | Test ID | Framework | Scenario |
|------|---------|-----------|----------|
| `test1_obedience_illogical.py` | 1 | Obedience | Illogical but runnable code; framed as own vs. weaker developer's |
| `test2_consistency_style.py`   | 2 | Consistency | Mixed documentation styles; explicit vs. implicit style guidance |
| `test3_obedience_broken.py`    | 3 | Obedience | Syntactically broken code; with and without suppressed commentary |
| `test4_resilience_repeat.py`   | 4 | Consistency / Resilience | Shallow author comments updated repeatedly in same session |

---

### How to run each test

1. Open a fresh Ollama session (e.g. `ollama run <model>`).
2. Copy the relevant **PROMPT_** constant from the bottom of each file.
3. Paste the file contents where instructed.
4. Save the full LLM response into `appendix_a/test<N>_round<M>.txt` for
   inclusion in Appendix A of your report.
5. Note any deviations in `appendix_b/test<N>_corrections.md` for Appendix B.

---

### Evaluation dimensions

| Dimension | What to look for |
|-----------|-----------------|
| **Obedience** | Does the model follow the instruction verbatim, or does it silently refactor / warn / deviate? |
| **Consistency** | Does output style match existing comments implicitly? Does it drift across a session? |
| **Usefulness** | Are comments meaningful and non-redundant? Do they add information beyond what the code already states? |

---

### Notes

- `test3_obedience_broken.py` is **intentionally broken Python** and should
  not be executed.  Errors are annotated with `# ← BUG`.
- All prompts are designed to be run against a **local Ollama instance** to
  respect the client's wishes regarding codebase privacy.
- The prompt injection attempts on page 6 of the PDF have been noted and are
  not included in these test files; they are relevant context for interpreting
  any unexpected model behaviour observed during testing.
