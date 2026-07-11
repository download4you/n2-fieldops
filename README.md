# Codex FieldOps

A production-minded `AGENTS.md` profile for Codex, combining pragmatic software engineering, evidence-driven CTF workflows, concise collaboration, UTF-8-safe PowerShell guidance, and stateful Prompt Decorators.

## Initial release: v2.0.0

- Prompt Decorators compatibility layer with 23 supported decorator names
- Message-scoped and persistent chat-scoped behavior
- State inspection and clearing with `+++ActiveDecs`, `+++AvailableDecs`, and `+++Clear`
- Complete user guide, decorator reference, examples, and troubleshooting
- GPT-5 / GPT-5.6 runtime awareness
- English as the default reply language
- Explicit UTF-8 handling for Persian (Farsi) text in PowerShell

## Highlights

- Outcome-first communication and low-noise progress updates
- Safe, reviewable file-editing and Git practices
- Explicit UTF-8 handling for console, pipelines, and file I/O
- Evidence-first CTF workflow across web, API, reverse engineering, pwn, crypto, DFIR, mobile, identity, Windows, and cloud challenges
- Inline decorators for reasoning style, planning, critique, formatting, tone, verification, conversation state, and export
- Runtime-aware instruction precedence and scoped autonomy

## Quick installation

Back up any existing project instructions, then copy the profile to the project root:

```powershell
$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

Copy-Item -LiteralPath '.\AGENTS.md' -Destination 'C:\path\to\project\AGENTS.md'
```

Start Codex from that project and verify decorator discovery:

```text
+++AvailableDecs
```

## Quick example

```text
+++MessageScope
+++Planning
+++Tone(style=technical)

Design a migration plan for this API.
```

To keep decorators active across later messages:

```text
+++ChatScope
+++Tone(style=technical)
+++Planning
```

Inspect or clear persistent state with `+++ActiveDecs` and `+++Clear`.

## Documentation

- [Complete user guide](docs/USER_GUIDE.md)
- [Prompt Decorators reference](docs/DECORATOR_REFERENCE.md)
- [Copy-ready examples](examples/README.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)

## Compatibility and precedence

Prompt Decorators are a prompting convention interpreted by the active model, not native executable commands. Exact behavior and chat-state retention depend on the Codex runtime and available context. System, platform, organization, developer, and more-specific repository instructions take precedence over this profile and its decorators.

The `+++Reasoning` decorator requests a useful explanation or structured rationale. It does not override platform rules concerning private internal reasoning.

## Attribution

The Prompt Decorators compatibility layer is adapted from [Prompt Decorators](https://github.com/smkalami/prompt-decorators) by Mostapha Kalami Heris and used under the MIT License. The upstream framework is described in [Prompt Decorators: A Declarative and Composable Syntax for Reasoning, Formatting, and Control in LLMs](https://arxiv.org/abs/2510.19850).

This project is independent and is not affiliated with or endorsed by the upstream author. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for the complete copyright and license notice.

## License

Original material in this repository is released under the [MIT License](LICENSE). Adapted third-party material remains subject to its original MIT notice.
