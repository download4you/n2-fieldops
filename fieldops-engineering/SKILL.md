---
name: fieldops-engineering
description: Diagnoses, implements, and verifies non-trivial or risk-sensitive changes in an existing repository while preserving the user's uncommitted work, following repository instructions (AGENTS.md or CLAUDE.md), keeping edits within authorized scope, and handing off with runtime evidence. Use when the user asks to fix a bug, add or change a feature, refactor, migrate, edit configuration, chase down a regression, or make a change safely amid overlapping edits or worktrees where verification and change control matter. Not for isolated code snippets or simple explanations; for diagnosis-only requests, prove and explain the cause without fixing unless asked.
---

# Engineering FieldOps

1. Classify authorization with `references/authorization.md`.
2. Read applicable repository instructions and inspect the worktree.
3. Establish current behavior with runtime evidence or a focused reproduction.
4. Identify the smallest coherent change.
5. Preserve unrelated edits and use reviewable patches.
6. Verify proportionally with `references/verification.md`.
7. Review the final diff for scope expansion.
8. Report outcome, files, verification, and unresolved risk.

Read `references/safe-editing.md` before Git or overlapping-file work. Prefer `rg` and focused reads. Never revert user changes, amend commits, or use destructive Git operations without explicit authority.
