---
name: fieldops-engineering
description: Diagnose, implement, and verify non-trivial or risk-sensitive changes in existing repositories while preserving user work, following repository instructions, limiting mutation to authorized scope, using reviewable patches, and producing evidence-backed handoffs. Use for bug fixes, features, refactors, migrations, configuration changes, overlapping worktrees, or investigations where verification and change control matter. Do not trigger for isolated code snippets or simple explanations. For diagnosis-only requests, prove and explain the cause without fixing unless requested.
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
