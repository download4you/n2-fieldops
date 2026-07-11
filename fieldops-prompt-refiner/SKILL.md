---
name: fieldops-prompt-refiner
description: Transform rough, ambiguous, overloaded, or reusable requests into precise execution-ready prompts for coding agents. Use when asked to improve, rewrite, structure, modularize, audit, or professionalize a prompt, AGENTS.md instruction set, task brief, or agent workflow. Preserve intent while clarifying outcome, scope, inputs, constraints, authority, verification, and deliverables. Do not use merely to answer a well-specified task.
---

# Prompt Refiner

1. Extract outcome, audience/agent, inputs, environment, and completion condition.
2. Separate hard constraints from preferences and examples.
3. Ask only about ambiguities that materially change safe execution.
4. Remove duplication, conflict, unenforceable claims, and low-value prose.
5. Organize with `references/prompt-architecture.md`.
6. Add proportional evidence and verification requirements.
7. Preserve language, terminology, intent, and authority boundary.
8. Return a copy-ready prompt plus a short design note when useful.

For large reusable profiles, prefer modular skills and references over one always-loaded prompt. Never claim a prompt can override higher-priority runtime instructions.
