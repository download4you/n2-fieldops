# FieldOps Claude adapter

This directory is the source template for the native Claude Code plugin. It is
intentionally kept free of `SKILL.md` files so CC Switch can recursively scan the
repository without discovering a second copy of every skill. The release builder
materializes the complete plugin under `dist/` and attaches it to the GitHub release.

Build locally from the repository root:

```powershell
py -3 scripts/build_release.py --output-dir dist
claude --plugin-dir .\dist\n2-fieldops-claude-plugin
```

The generated plugin contains all 17 canonical skills, a Claude manifest, the
optional `CLAUDE_PROFILE.md`, and standalone license/provenance notices. The same
root skill tree can also be installed directly into Claude and Codex through CC
Switch.

The prompts are model-neutral and work with the current Claude Opus family and
current Codex GPT/Codex models. Select the model exposed by the client; this adapter
does not pin a version-specific model identifier.
