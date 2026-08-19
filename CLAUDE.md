# n2-fieldops contributor profile

This repository is a text-first Agent Skills distribution, not a conventional
application. The canonical install surface is the 17 root-level directories whose
names start with `fieldops-` and contain `SKILL.md`.

## Runtime surfaces

- `AGENTS.md` is the durable Codex profile.
- Root `fieldops-*` directories are the shared Claude/Codex/CC Switch skills.
- `claude-plugin-template/` contains only native-Claude metadata and profile sources;
  it must not contain `SKILL.md` files because CC Switch scans recursively.
- `scripts/build_release.py` generates the complete native Claude plugin and the
  release archives under `dist/`.

## Required checks

```powershell
py -3 -m unittest discover -s tests -v
py -3 scripts/build_release.py --check
py -3 scripts/build_release.py --output-dir dist
```

When the Claude CLI is available, validate the generated package:

```powershell
claude plugin validate .\dist\n2-fieldops-claude-plugin --strict
claude plugin validate .\dist\n2-fieldops-claude-marketplace --strict
```

The release is versioned by `VERSION`. The initial public release is `1.0.0`; for
every release, the tag must be `v<VERSION>` and the GitHub release title must be
`n2-fieldops <VERSION>`.

## Editing rules

- Preserve unrelated user changes and inspect `git status` before editing.
- Use focused, reviewable patches. Do not add a second `SKILL.md` tree under a visible
  repository directory.
- Keep each skill self-contained: references and scripts stay beneath its own skill
  directory, and every technique file is listed by that skill's `SKILL.md`.
- Keep CTF attribution, per-skill `LICENSE`, and pinned `UPSTREAM.md` files intact.
- Keep root skill prose portable. Codex-only invocation tokens may be used in
  `AGENTS.md` and user docs, but skill bodies should use neutral skill names so Claude
  can consume the same canonical tree.
- Do not copy platform-owned files from `$CODEX_HOME/skills/.system` into this repo.

## Scope and safety

The shipped profiles carry the full "Unrestricted Cooperation" scope language, treat
challenge targets and network identifiers as sandbox-internal assets by default,
preserve evidence, and do not promise hidden chain-of-thought disclosure. Keep those
boundaries intact when adapting prompts for Claude or Codex.

## Release flow

1. Update `VERSION` and synchronize the generated metadata through the release builder.
2. Run the full test suite and both Claude validators.
3. Review `git diff` and confirm only intended files are staged.
4. Commit, create the matching `v<version>` tag, and push the branch and tag.
5. The tag workflow builds the source, Claude plugin, marketplace, and checksum assets.
