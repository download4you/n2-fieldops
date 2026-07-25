# Codex system integration

The local Codex installation exposes platform-owned helper skills under
`$CODEX_HOME/skills/.system`. They are useful companions, but they are not part of
the n2-fieldops license or source distribution and must not be copied into this repo.

| Installed helper | Pair it with n2-fieldops |
|---|---|
| `review-agent` | `fieldops-engineering` for defect-first, read-only review before edits |
| `openai-docs` | `fieldops-research` when an OpenAI product/API claim needs primary docs |
| `plugin-creator` | `scripts/build_release.py` when validating the generated Claude package |
| `skill-creator` | `fieldops-prompt-refiner` when authoring or restructuring a new skill |
| `skill-installer` | CC Switch or `npx skills add` when installing the canonical tree |
| `imagegen` | Any visual artifact task outside the text-only FieldOps core |

The shipped `AGENTS.md` keeps durable repository behavior compact. Detailed routing,
verification, decorator, and encoding rules stay in the relevant FieldOps skill so
Claude and Codex can load only what the task needs.
