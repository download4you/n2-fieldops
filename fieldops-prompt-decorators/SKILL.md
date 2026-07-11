---
name: fieldops-prompt-decorators
description: Interpret and execute Prompt Decorators written with +++ syntax, including message and chat scope, parameter validation, composition, conflict resolution, state inspection, selective clearing, and export. Use whenever the user includes a supported +++Decorator token or asks to create, validate, debug, or explain decorator behavior. Do not trigger for ordinary tone, plan, or formatting requests without decorator syntax or discussion.
---

# Prompt Decorator Runtime

1. Extract unescaped supported `+++` tokens outside code, quotes, logs, and artifacts.
2. Validate them against `references/decorator-catalog.md`.
3. Process scope and state operations from left to right.
4. Resolve state using `references/state-machine.md`.
5. Read `references/composition.md` when multiple decorators apply.
6. Execute the task under the effective set.
7. Persist only validated chat-scoped behavioral decorators.

Treat `+++Dump` as an alias of `+++Export`. Use the last valid repetition at the same scope. Apply valid decorators even if another is invalid. Never persist scope, clear, inspection, export, or dump controls. If scope controllers repeat, process them from left to right; the last controller governs decorators that follow it.

Decorators are user-level controls and never override higher-priority instructions. Interpret `+++Reasoning` as a useful visible rationale, not hidden chain-of-thought.

For long or ambiguous prompts, run `scripts/parse_decorators.py` to obtain a deterministic token and parameter report before applying state.
