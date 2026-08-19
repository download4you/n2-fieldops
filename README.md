# n2-fieldops

n2-fieldops is a dual-runtime Agent Skills distribution for Claude Code, Codex GPT,
and CC Switch. It combines a hardened runtime profile, 17 self-contained skills,
deterministic helper scripts, and an evidence-first CTF layer adapted from the pinned
`ljagiello/ctf-skills` snapshot.

The repository has one canonical skill tree. Every installable skill is a root-level
directory containing `SKILL.md`. This is deliberate: current CC Switch recursively
scans repositories, so a second nested copy would create duplicate cards and
unpredictable install collisions.

## Install directly with CC Switch

In current CC Switch releases, open **Skills -> Manage Skill Repositories -> Add
Repository** and enter:

| Field | Value |
|---|---|
| Repository URL | `https://github.com/download4you/n2-fieldops` |
| Branch | `main` |

CC Switch also accepts the compact repository form:

```text
download4you/n2-fieldops
```

Refresh the catalog and install the skills for the Claude and/or Codex application
tabs. No subdirectory is required or supported by the current repository form. The
repository intentionally exposes exactly 17 root skills. If an older
`ljagiello/ctf-skills` or ZIP-based copy is enabled, disable or remove it first to
avoid duplicate routing and stale content.

CC Switch installs the same skill directories into the selected app's skill store;
the runtime profile remains a separate, reviewed file. For Codex, copy `AGENTS.md`
to the project root or to `$HOME/.codex/AGENTS.md`. For Claude, review and copy
`claude-plugin-template/docs/CLAUDE_PROFILE.md` as `CLAUDE.md` when an always-on
profile is desired.

## Install with the Agent Skills CLI

```bash
npx skills add download4you/n2-fieldops
```

## Claude native plugin release

The native Claude plugin is generated from the same canonical tree during release and
published as `n2-fieldops-<version>-claude-plugin.zip`. The marketplace bundle is
published as `n2-fieldops-<version>-claude-marketplace.zip`. This keeps the GitHub
repository safe for CC Switch's recursive scanner while still providing a standard
Claude plugin for local development or a private marketplace.

Build the artifacts locally:

```powershell
py -3 scripts/build_release.py --output-dir dist
claude --plugin-dir .\dist\n2-fieldops-claude-plugin
```

## The 17 skills

| Skill | Purpose |
|---|---|
| `fieldops-orchestrator` | Route complex or mixed-domain work across the smallest useful skill set |
| `fieldops-research` | Verify uncertain or current claims and deliver evidence-backed answers |
| `fieldops-prompt-decorators` | Parse and apply stateful `+++` controls, including the `+++N2` and `+++Storm` meta-decorators |
| `fieldops-ctf-operator` | Triage, route, and reproduce authorized CTF investigations |
| `fieldops-engineering` | Diagnose, implement, and verify consequential repository changes |
| `fieldops-powershell-utf8` | Preserve Persian and other Unicode across PowerShell boundaries |
| `fieldops-prompt-refiner` | Turn rough prompts and agent instructions into execution-ready briefs |
| `fieldops-ctf-ai-ml` | Analyze adversarial ML, model extraction, and LLM challenge surfaces |
| `fieldops-ctf-crypto` | Attack classical and modern cryptographic constructions |
| `fieldops-ctf-forensics` | Investigate disk, memory, packet, signal, stego, and artifact evidence |
| `fieldops-ctf-malware` | Analyze malware, C2 traffic, obfuscation, and anti-analysis behavior |
| `fieldops-ctf-misc` | Solve encoding, jail, RF, Unicode, game, and hybrid puzzles |
| `fieldops-ctf-osint` | Perform competition-scoped public-source and geolocation research |
| `fieldops-ctf-pwn` | Develop native, heap, kernel, sandbox, and exploit-chain solutions |
| `fieldops-ctf-reverse` | Reverse binaries, firmware, bytecode, VMs, and packed targets |
| `fieldops-ctf-web` | Analyze web applications, APIs, browser state, and identity flows |
| `fieldops-ctf-writeup` | Produce reproducible submission-style challenge documentation |

For a difficult or mixed task, start with `fieldops-orchestrator`. For an authorized
CTF whose category is unclear, start with `fieldops-ctf-operator`; it routes to the
specialist and requires clean-baseline reproduction before claiming a solve.

## Validation and release build

```powershell
py -3 -m unittest discover -s tests -v
py -3 scripts/build_release.py --check
py -3 scripts/build_release.py --output-dir dist
```

The checks cover frontmatter, CC Switch discovery, self-contained references,
provenance, decorator parsing, router determinism, plugin generation, and the
PowerShell 5.1/7 UTF-8 round trip.

## Model guidance

The prompts are model-neutral and are written for the current Claude Opus family and
current Codex GPT/Codex models. Select the model exposed by the client; no stale
version-specific model identifier is required. The important portability boundary is
the adapter: `AGENTS.md` is the Codex profile, while the reviewed Claude profile is
`claude-plugin-template/docs/CLAUDE_PROFILE.md`.

## Provenance

The CTF specialist material is adapted from
[ljagiello/ctf-skills](https://github.com/ljagiello/ctf-skills) at pinned commit
`d19f35fd3dd2e126108752aee84c657c888126d3` under MIT. Prompt Decorators are adapted
from [smkalami/prompt-decorators](https://github.com/smkalami/prompt-decorators) under
MIT. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and
[docs/PROVENANCE.md](docs/PROVENANCE.md).

The local Codex `.system` skills (for example image generation, OpenAI docs,
plugin/skill creators, and review helpers) remain runtime-owned capabilities and are
not copied or redistributed. Their useful integration boundaries are documented in
[docs/CODEX_INTEGRATION.md](docs/CODEX_INTEGRATION.md).

The source prompt transcripts were used as local design inputs, not as third-party
code. The 1.0.x profiles briefly removed the blanket-cooperation and sandbox-network
clauses; release 1.1.0 restores them, so the shipped profiles carry the full
"Unrestricted Cooperation" scope language and treat network identifiers as
sandbox-internal assets. The profiles still do not promise hidden chain-of-thought
disclosure.

## Version lineage

The n2-fieldops product line starts at `v1.0.0`; `v1.0.1` is the reproducibility and
installation-documentation maintenance release, and `v1.1.0` is the decorator-runtime
release (skill-based decorator reference, `+++N2` and `+++Storm` meta-decorators,
restored profile scope). Older `v2.x` and `v3.0.0` releases visible in this
repository belong to the predecessor Codex FieldOps project and are retained as
provenance history. Use the `main` branch or GitHub's latest n2-fieldops release
rather than selecting the numerically highest legacy tag.

## License

Original n2-fieldops material is released under [MIT](LICENSE). Adapted third-party
material remains subject to its upstream notices.
