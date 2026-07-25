# Build and provenance record

This document records the inputs and transformations used for the n2-fieldops 1.0.x
release line, including the reproducibility patch shipped in 1.0.1.

## Inputs

- The previous FieldOps repository baseline (`v3.0.0`) and its existing tests.
- The upstream CTF material from
  `https://github.com/ljagiello/ctf-skills` at commit
  `d19f35fd3dd2e126108752aee84c657c888126d3` (MIT).
- Prompt Decorator material adapted from
  `https://github.com/smkalami/prompt-decorators` at reviewed revision
  `365c065b7a061a5a3c2fb7984a99c56d4dd65991` (MIT).
- Local prompt transcripts supplied during design review. They were treated as
  authoring inputs only; they contain no independently redistributable source tree or
  license manifest and are not copied into the release.
- The local Codex system skills and `.codex/AGENTS.md` were inspected for integration
  ideas. Platform-owned `.system` files and the permissive legacy profile are not
  redistributed.

## Transformations

- Added the seven FieldOps workflow skills and the CTF operator/reproduction contract.
- Namespaced adapted CTF skills under `fieldops-ctf-*`, preserving each upstream
  `LICENSE` and `UPSTREAM.md` file.
- Hardened authorization and network assumptions; removed blanket authorization,
  fictional-network, and hidden-reasoning promises from shipped profiles.
- Moved portable trigger guidance into each skill description and neutralized
  Codex-only skill tokens in the canonical skill prose so the same tree works in
  Claude and Codex.
- Added deterministic router, decorator parser, and PowerShell UTF-8 checks.
- Added a release builder that materializes the native Claude plugin only in release
  artifacts, preventing duplicate recursive discovery by CC Switch.
- Made release archives cross-platform reproducible by normalizing text, fixing ZIP
  ordering/metadata, and limiting source archives to tracked Git files.
- Updated the CC Switch installation path to the current Repository URL + Branch UI.
- Started the renamed n2-fieldops product line at `v1.0.0`; predecessor `v2.x` and
  `v3.0.0` tags are retained as historical Codex FieldOps provenance.

## Verification evidence

- Upstream payload comparison found all 107 technique/reference files present; the
  small differences are path namespacing or formatting-only adaptations.
- The repository test suite validates frontmatter, self-contained links, provenance,
  deterministic helpers, and the one-copy CC Switch layout.
- In this review, `claude plugin validate --strict` passed for both the generated
  plugin and generated marketplace bundle. GitHub CI validates the deterministic
  builder and can add the CLI check when a runner provides Claude Code.
