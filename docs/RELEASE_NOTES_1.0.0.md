# n2-fieldops 1.0.0

Initial n2-fieldops release: a single canonical skill tree for Claude Code, Codex GPT,
and direct CC Switch installation.

## Highlights

- 17 self-contained FieldOps skills with improved trigger descriptions and routing
  hints.
- Complete adapted CTF specialist layer pinned to `ljagiello/ctf-skills` commit
  `d19f35fd3dd2e126108752aee84c657c888126d3` with per-skill MIT provenance.
- Hardened `AGENTS.md` for Codex and a separate model-neutral Claude profile.
- Deterministic CTF router, Prompt Decorator parser, and PowerShell UTF-8 validator.
- CC Switch-safe layout with no nested duplicate `SKILL.md` tree.
- Deterministic source, Claude plugin, Claude marketplace, and SHA-256 assets.

## CC Switch installation

In **Skills -> Manage Skill Repositories -> Add Repository**, use Repository URL
`https://github.com/download4you/n2-fieldops` and branch `main`. The current CC Switch
repository form has no subdirectory field. Refresh the catalog and enable the desired
skills for Claude and/or Codex. Disable older `ctf-skills` or ZIP copies first to avoid
duplicate names.

## Release assets

- `n2-fieldops-1.0.0-source.zip`
- `n2-fieldops-1.0.0-claude-plugin.zip`
- `n2-fieldops-1.0.0-claude-marketplace.zip`
- `SHA256SUMS`
