# Runtime compatibility

## Canonical source

The 17 directories at repository root are the only CC Switch discovery surface. Each
contains one `SKILL.md` plus its references and scripts. Do not add a second copy under
another visible directory in this repository: CC Switch recursively scans all folders.

| Consumer | Install surface | Always-on profile |
|---|---|---|
| CC Switch + Codex | Root `fieldops-*` directories | Copy `AGENTS.md` if desired |
| CC Switch + Claude | The same root `fieldops-*` directories | Copy `claude-plugin-template/docs/CLAUDE_PROFILE.md` if desired |
| Codex CLI | `~/.codex/skills/` or project `.codex/skills/` | `AGENTS.md` |
| Kimi CLI | `~/.kimi/skills/` (merged with `~/.claude/skills/` and `~/.codex/skills/` when present) | `KIMI.md` |
| Claude Code | `~/.claude/skills/` or project `.claude/skills/` | `CLAUDE_PROFILE.md` as `CLAUDE.md` |
| Native Claude plugin | Release artifact `*-claude-plugin.zip` | Profile is shipped as a reference document |

## Clean CC Switch test

1. Open **Skills -> Manage Skill Repositories -> Add Repository**.
2. Enter repository URL `https://github.com/download4you/n2-fieldops` and branch
   `main`. The current CC Switch repository form has no subdirectory field.
3. Refresh the repository catalog.
4. Confirm exactly 17 FieldOps cards are listed.
5. Disable older `ljagiello/ctf-skills` or ZIP copies before installing the matching
   names, otherwise stale cards can win the install-name collision.
6. Enable the installed skills for the Claude and/or Codex application tab.

## Native Claude artifact

Run `py -3 scripts/build_release.py` and use the generated
`n2-fieldops-<version>-claude-plugin.zip` for `claude --plugin-dir`, or use the
generated marketplace bundle for a local Claude marketplace. The generated package is
kept out of the main source tree specifically to preserve CC Switch's one-copy rule.

## Model portability

The skill descriptions and profiles avoid version-pinned model identifiers. They are
intended for the current Claude Opus family and current Codex GPT/Codex models; model
selection remains a client configuration choice.
