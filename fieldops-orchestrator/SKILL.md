---
name: fieldops-orchestrator
description: Coordinates multiple FieldOps skills for complex, unfamiliar, or mixed-domain work spanning research, prompt control, authorized CTF evidence, repository changes, PowerShell Unicode handling, or prompt refinement. Use when a task needs two or more FieldOps workflows, when the correct specialist is unclear, or when the user invokes fieldops-orchestrator. Prefer a narrower skill for clearly single-domain tasks.
---

# FieldOps Orchestrator

1. Define the concrete outcome and authorized scope.
2. Classify workstreams with `references/routing.md`.
3. Select the smallest set of specialist skills.
4. Order dependencies: controls, inspection, implementation, verification, report.
5. For unfamiliar questions, route evidence gathering through `fieldops-research`.
6. Maintain one ledger for assumptions, artifacts, decisions, and results.
7. Stop at the requested mutation boundary.
8. Deliver outcome, evidence, verification, and uncertainty.

Read and follow every selected skill completely. Do not duplicate its instructions or activate all skills by default. Preserve originals and unrelated work, prefer runtime evidence, use explicit UTF-8 boundaries for multilingual PowerShell, and require reproducible verification. When no specialist skill exists, decompose the task, use available tools directly, and keep the same evidence and verification contract.
