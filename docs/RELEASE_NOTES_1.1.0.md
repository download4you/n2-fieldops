# n2-fieldops 1.1.0

Feature release: skill-based Prompt Decorator runtime with the `+++N2` and `+++Storm`
meta-decorators, and a token-optimized Codex profile.

## New

- Meta-decorators `+++N2` (deep rigorous analysis) and `+++Storm` (novel-idea
  generation): each treats `+++ChatScope` as active first, then activates its defined
  decorator stack. Full expansion, parameters, and deactivation rules ship in the
  `fieldops-prompt-decorators` skill at `references/meta-decorators.md`.
- The decorator catalog, state machine, composition rules, docs reference, and the
  deterministic parser (`scripts/parse_decorators.py`) all validate and document
  `N2`/`Storm` parameters (`iterations`, `limit`, `diversity`, `lens`, `domain`).

## Profile updates

- `AGENTS.md` (Codex profile) is now skill-based and token-optimized (417 -> 189
  lines): the decorator reference moved into the `fieldops-prompt-decorators` skill,
  while runtime awareness keeps natural-language activation, decorator precedence,
  one-line acknowledgements, and the mandatory `[Active: ...]` state line with a
  re-read rule after context compaction.
- Restored profile sections: Scope and Cooperation, Reverse Engineering and Malware
  (11-step block), Engineering Quality and Token Efficiency, and Idea Generation and
  Novel Concepts.
- `claude-plugin-template/docs/CLAUDE_PROFILE.md` gained the same decorator-runtime
  capabilities (natural-language activation, meta-decorator expansion, the
  `[Active: ...]` state line, `N2`/`Storm` parameter limits) and the same uncensored
  stance as the Codex profile: full Scope and Cooperation language, sandbox-internal
  network identifiers, and CTF targets treated as authorized sandbox assets by
  default. The 1.0.x hardening of authorization and network assumptions is reverted.

## Compatibility

The canonical repository remains one root-level tree with exactly 17 `SKILL.md`
directories. Install from CC Switch with:

```text
Repository URL: https://github.com/download4you/n2-fieldops
Branch: main
```

The native Claude plugin and marketplace bundles are generated from the same
canonical tree.

## Release assets

- `n2-fieldops-1.1.0-source.zip`
- `n2-fieldops-1.1.0-claude-plugin.zip`
- `n2-fieldops-1.1.0-claude-marketplace.zip`
- `SHA256SUMS`
