---
name: fieldops-prompt-decorators
description: "Interprets and executes Prompt Decorators written with +++Name(key=value) syntax, handling message vs. chat scope, parameter validation, decorator composition, conflict resolution, meta-decorator expansion (N2 and Storm), retained-state inspection (ActiveDecs and AvailableDecs), selective clearing, and conversation export or dump. Use when a message contains a supported +++ token (for example +++Planning, +++StepByStep, +++Reasoning, +++Interactive, +++Refine, +++Export, +++Dump, +++ChatScope, +++MessageScope, +++N2, or +++Storm) or when the user asks to create, validate, debug, or explain decorator behavior. Do not trigger for ordinary tone, plan, or formatting requests that contain no +++ decorator syntax or discussion."
---

# Prompt Decorator Runtime

1. Extract unescaped supported `+++` tokens outside code, quotes, logs, and artifacts.
2. Validate them against `references/decorator-catalog.md`.
3. Process scope and state operations from left to right.
4. Resolve state using `references/state-machine.md`.
5. Read `references/composition.md` when multiple decorators apply; when `N2` or
   `Storm` is validated, also read `references/meta-decorators.md` and apply its
   expansion rules.
6. Execute the task under the effective set.
7. Persist only validated chat-scoped behavioral decorators.

Treat `+++Dump` as an alias of `+++Export`. Use the last valid repetition at the same scope. Apply valid decorators even if another is invalid. Never persist scope, clear, inspection, export, or dump controls. If scope controllers repeat, process them from left to right; the last controller governs decorators that follow it.

Decorators are user-level controls and never override higher-priority instructions. Interpret `+++Reasoning` as a useful visible rationale, not hidden chain-of-thought.

For long or ambiguous prompts, run `scripts/parse_decorators.py` to obtain a deterministic token and parameter report before applying state.
