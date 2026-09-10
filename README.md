# PROVE IT — Day 01: Find the Problem

Day 01 mission from the PROVE IT competition (Arabian Academy — AI Engineering Track): find and fix a hidden bug in a simple Python AI pipeline.

## Original Code (`before`)

The `SimpleAIPipeline` class receives a user prompt, validates its length, stores it in `history`, and has a `get_average_prompt_length()` method that computes the average length of previous prompts.

## The Bug

`get_average_prompt_length()` divides `total_length` by `len(self.history)` without checking whether there's any data at all:

```python
def get_average_prompt_length(self):
    total_length = sum([len(item["echo"]) for item in self.history])
    return total_length / len(self.history)
```

If the method is called before any `process_input()` call, `self.history` is `[]`, so `len(self.history) = 0`, and this happens:

```
ZeroDivisionError: division by zero
```

**Proof:** verified by actually running the code — a fresh `SimpleAIPipeline` instance, then calling `get_average_prompt_length()` directly with no prior prompt. The code crashed immediately with the exact same error.

**Why it matters in production:** any other part of the system (a dashboard, a monitoring tool) could call this method before the first real request ever arrives, taking down the whole service from the very first second.

## The Fix (`after`)

```python
def get_average_prompt_length(self):
    if not self.history:
        return 0.0
    total_length = sum(len(item["echo"]) for item in self.history)
    return total_length / len(self.history)
```

A guard clause checks whether `history` is empty before dividing, and returns `0.0` instead of crashing — this fixes the root cause (missing validation) instead of just wrapping it in a `try/except` that catches the exception after it happens.

## Additional Improvements Made in `after`

| Improvement | Why |
|---|---|
| Confirm the input is actually a `string` | Previously crashed with `AttributeError` on `None` |
| Real token estimate instead of counting characters | `max_tokens` was measuring characters, not actual tokens |
| `deque(maxlen=...)` instead of a plain `list` | Prevents a memory leak from history growing without bound |
| All errors return a `{"status": "error", ...}` dict | Makes the error shape consistent with the success shape, instead of an inconsistent `raise` |
| Removed unused `import json` + `sum()` now uses a generator | Cleans up the code and saves memory |

## Files

| File | Description |
|---|---|
| `simple_ai_pipeline_before.py` / `.ipynb` | The original code exactly as given in the mission |
| `simple_ai_pipeline_after.py` / `.ipynb` | The code after all fixes, with each change commented with its reasoning |
