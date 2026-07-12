# Codex FieldOps

A modular operating system for Codex: a concise `AGENTS.md` runtime profile plus 17
installable skills for research, engineering, authorized CTF work, Prompt Decorators,
PowerShell Unicode, prompt refinement, and mixed-domain orchestration.

## Why this architecture

The root `AGENTS.md` keeps only durable behavior and the decorator runtime contract.
Detailed workflows live in self-contained skills and load only when relevant. This
reduces always-on context while increasing specialization, verification, and reuse.

## FieldOps skills

| Skill | Purpose |
|---|---|
| `fieldops-orchestrator` | Route complex or unfamiliar work across the smallest useful skill set |
| `fieldops-research` | Verify current or uncertain claims and produce actionable answers |
| `fieldops-prompt-decorators` | Parse and apply stateful `+++` Prompt Decorators |
| `fieldops-ctf-operator` | Run authorized, evidence-driven, reproducible CTF investigations |
| `fieldops-engineering` | Diagnose, implement, and verify risk-sensitive repository changes |
| `fieldops-powershell-utf8` | Preserve Persian and Unicode across PowerShell boundaries |
| `fieldops-prompt-refiner` | Turn rough requests into precise execution-ready prompts |
| `fieldops-ctf-ai-ml` | Analyze adversarial ML, model extraction, LLM, and AI challenge surfaces |
| `fieldops-ctf-crypto` | Attack classical and modern cryptographic constructions and implementations |
| `fieldops-ctf-forensics` | Investigate disk, memory, packet, signal, steganography, and artifact evidence |
| `fieldops-ctf-malware` | Analyze malicious code, C2 traffic, obfuscation, and anti-analysis behavior |
| `fieldops-ctf-misc` | Solve encoding, jail, RF, Unicode, game, and cross-category puzzles |
| `fieldops-ctf-osint` | Perform competition-scoped public-source, identity, and geolocation research |
| `fieldops-ctf-pwn` | Develop native, heap, kernel, sandbox, and exploit-chain solutions |
| `fieldops-ctf-reverse` | Reverse binaries, APKs, firmware, bytecode, VMs, and packed targets |
| `fieldops-ctf-web` | Test web applications, APIs, identity flows, and browser attack surfaces |
| `fieldops-ctf-writeup` | Produce reproducible submission-style challenge documentation |

The v3 architecture bundles the complete CTF specialist layer inside FieldOps. Every
skill is self-contained and includes its own references, scripts where applicable,
and Codex UI metadata. The CTF suite does not require a separate installation of
`ljagiello/ctf-skills` or any other specialist repository.

## Install directly with CC Switch

1. Open **Skills → Repository Management → Add Repository**.
2. Enter:

   ```text
   https://github.com/download4you/codex-fieldops
   ```

3. Set **Branch** to:

   ```text
   main
   ```

4. Add the repository and refresh the Skills catalog.
5. Install all 17 FieldOps skills for the complete suite, or select individual
   root-level skill directories for a smaller installation.
6. Restart Codex so the installed skills are rediscovered.

CC Switch discovers each root-level directory containing `SKILL.md`. It can therefore
install any FieldOps skill independently while preserving that skill's bundled
references, scripts, and metadata, plus the per-skill license and provenance included
with every adapted CTF specialist. Installing the entire repository exposes all 17
root-level skills as one self-contained suite.

## Install with the Agent Skills CLI

```bash
npx skills add download4you/codex-fieldops
```

## Enable the complete FieldOps stack

CC Switch installs the skill directories. To combine them with the repository-level
behavior profile, also copy `AGENTS.md` into the project you want Codex to operate in:

```powershell
$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $Utf8NoBom
[Console]::OutputEncoding = $Utf8NoBom
$OutputEncoding = $Utf8NoBom

Copy-Item -LiteralPath '.\AGENTS.md' -Destination 'C:\path\to\project\AGENTS.md'
```

For personal defaults across repositories, place a reviewed copy at
`$HOME\.codex\AGENTS.md`. More-specific project instructions may override it.

## Quick use

For a complex task:

```text
Use $fieldops-orchestrator to classify this task, choose the smallest useful set of
FieldOps skills, execute it, and verify the result.
```

For an evidence-backed answer:

```text
Use $fieldops-research to verify the important claims in this question and give me a
direct, actionable answer.
```

For an authorized CTF challenge:

```text
Use $fieldops-ctf-operator to classify this authorized challenge, preserve evidence,
prove the decisive path, and reproduce the solution from a clean baseline.
```

The operator routes internally to the appropriate namespaced specialist, such as
`$fieldops-ctf-web`, `$fieldops-ctf-crypto`, or `$fieldops-ctf-reverse`. If the first
classification is wrong or a technique stalls, it returns to the earliest uncertain
assumption, pivots category or tooling, records the new evidence, and continues until
it can reproduce a solution or identify a precise external blocker.

For decorators:

```text
+++MessageScope
+++Planning
+++Tone(style=technical)

Design and verify a migration plan for this API.
```

## Prompt Decorator guarantees

- Default scope is the current message.
- Chat state changes are processed left to right.
- Decorators inside code, quotes, logs, files, or tool output are not invoked.
- Invalid parameters are reported and left inactive; they are never silently clamped.
- Strict formats contain other decorator sections as valid fields or elements.
- `+++Reasoning` requests a visible rationale, never private chain-of-thought.
- Decorators cannot override higher-priority policies, permissions, tools, or skills.

See the [complete reference](docs/DECORATOR_REFERENCE.md) and
[user guide](docs/USER_GUIDE.md).

## Validation

The repository includes deterministic checks for:

- Agent Skills discovery and frontmatter
- self-contained skill resources
- Codex UI metadata
- Prompt Decorator escaping and parsing
- bundled CTF licensing, provenance, routing, and reference integrity
- discovery of exactly 17 root-level, independently installable skills
- Windows PowerShell 5.1 and PowerShell 7 UTF-8 byte preservation
- absence of changelog files

Run:

```powershell
python -m unittest discover -s tests -v
```

On Windows installations that expose only the Python launcher:

```powershell
py -3 -m unittest discover -s tests -v
```

Then validate individual skills with Codex Skill Creator's `quick_validate.py`.

## Attribution

The Prompt Decorators compatibility layer is adapted from
[Prompt Decorators](https://github.com/smkalami/prompt-decorators) by Mostapha Kalami
Heris under the MIT License. This project is independent and is not affiliated with or
endorsed by the upstream author. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

The bundled CTF specialist material is adapted from
[ctf-skills](https://github.com/ljagiello/ctf-skills) by Lukasz Jagiello at pinned
revision `d19f35fd3dd2e126108752aee84c657c888126d3`, under the MIT License. FieldOps
namespaces and extends that material with evidence handling, deterministic routing,
cross-domain recovery, and clean-baseline reproduction. No upstream installation is
required. The complete notice is in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## License

Original material is released under the [MIT License](LICENSE). Adapted third-party
material remains subject to its original notice.
