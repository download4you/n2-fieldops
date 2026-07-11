# Complete User Guide

## 1. Overview

Codex FieldOps is a reusable `AGENTS.md` configuration for Codex. It combines:

- Pragmatic software-engineering behavior
- Clear collaboration and progress reporting
- Safe file and Git practices
- Explicit PowerShell UTF-8 handling for Persian text
- Evidence-driven CTF workflows
- Stateful inline Prompt Decorators

Prompt Decorators are markers such as `+++Planning` or `+++Tone(style=technical)` placed in a user message. They influence the response for one message or, with chat scope, for later messages in the same conversation.

They are interpreted instructions, not executable commands or a native parser. The active runtime and higher-priority instructions always remain authoritative.

## 2. Installation

### Project-level installation

1. Back up an existing `AGENTS.md` if the project already has one.
2. Copy this repository's `AGENTS.md` into the project root.
3. Start Codex from that directory.
4. Test the installation with `+++AvailableDecs`.

PowerShell example:

```powershell
$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

$source = '.\AGENTS.md'
$destination = 'C:\path\to\project\AGENTS.md'

if (Test-Path -LiteralPath $destination) {
    Copy-Item -LiteralPath $destination -Destination "$destination.backup"
}

Copy-Item -LiteralPath $source -Destination $destination
```

### Nested instructions

You may add a more specific `AGENTS.md` under a subdirectory for local rules. The exact discovery and precedence behavior depends on the Codex runtime. Review parent and nested files when behavior appears inconsistent.

## 3. First use

Use a message-scoped decorator for a single request:

```text
+++MessageScope
+++StepByStep
+++Tone(style=technical)

Explain how this authentication flow works.
```

Activate persistent chat-scoped decorators:

```text
+++ChatScope
+++Planning
+++Tone(style=technical)
```

Later requests in the same conversation inherit the active chat decorators until they are cleared, changed, paused for a message, or the conversation context is reset.

Inspect state:

```text
+++ActiveDecs
```

Clear selected state:

```text
+++Clear(+++Planning, +++Tone)
```

Clear all persistent decorators:

```text
+++Clear
```

## 4. Syntax

Basic form:

```text
+++DecoratorName
```

Parameterized form:

```text
+++DecoratorName(key=value, key2=value2)
```

Stack decorators by placing one per line before the task:

```text
+++MessageScope
+++Critique
+++Candor(level=high)
+++OutputFormat(format=markdown)

Review this design proposal.
```

Use the exact decorator spelling shown in the reference. Parameter values should match documented options. Quote multi-word string values when useful, for example `+++Import(topic="Systems Thinking")`.

## 5. Scope and state lifecycle

### Message scope

`+++MessageScope` applies the decorators in that message only. The source profile specifies that existing chat-scoped decorators are paused, not erased, for that message.

### Chat scope

`+++ChatScope` activates decorators from the same message at conversation scope. They persist across later turns while the conversation retains the relevant context.

### Clearing and inspection

- `+++Clear` clears all active chat-scoped decorators.
- `+++Clear(+++Name, +++OtherName)` clears selected decorators.
- `+++ActiveDecs` lists active chat-scoped decorators.
- `+++AvailableDecs` lists every supported decorator and its active/inactive state.

### Example lifecycle

1. Send `+++ChatScope`, `+++Tone(style=technical)`, and `+++Planning`.
2. A normal request inherits technical tone and planning.
3. Send `+++MessageScope` with `+++OutputFormat(format=json)` for one JSON-only response. The stored chat decorators are paused for that message, not deleted.
4. Send `+++Clear(+++Tone)` to remove the persistent tone while leaving planning active.
5. Send `+++ActiveDecs` to verify state.

Chat-scoped state normally ends when the conversation is reset or when the host no longer retains the relevant context.

## 6. Combining decorators

Decorators may be stacked when their requirements are compatible.

### Research and verification

```text
+++MessageScope
+++FactCheck
+++CiteSources
+++OutputFormat(format=markdown)

Assess these technical claims.
```

### Design review

```text
+++MessageScope
+++Critique
+++Candor(level=high)
+++Tone(style=technical)

Review this architecture.
```

### Ideation followed by refinement

```text
+++MessageScope
+++Brainstorm(limit=5, diversity=high)

Generate deployment strategies for this service.
```

Then, in a later message:

```text
+++MessageScope
+++Critique
+++Refine(iterations=3)

Evaluate and improve the strongest two strategies.
```

### Systems analysis

```text
+++MessageScope
+++Import(topic="Systems Thinking")
+++Debate

Analyze whether this monolith should be split into services.
```

## 7. Precedence and conflicts

Use these practical rules when decorators overlap:

1. System, platform, organization, developer, and applicable repository instructions take precedence.
2. The explicit user task and constraints come before optional stylistic decorators.
3. A strict output format should represent required sections as fields when possible. For example, a JSON response can contain `plan`, `steps`, and `sources` keys.
4. If the same parameterized decorator appears more than once, the last clearly specified value should be treated as the intended value unless a higher-priority instruction says otherwise.
5. Avoid placing `+++ChatScope` and `+++MessageScope` in the same message because the source profile does not define an unambiguous collision rule.
6. `+++Socratic` and `+++Interactive` may require questions before execution; do not combine them with a request that forbids questions unless you define which behavior should win.
7. `+++Tone` changes presentation, not factuality, required format, or instruction priority.
8. `+++Reasoning` requests a user-visible rationale or explanation, not private hidden chain-of-thought.
9. `+++CiteSources` and `+++FactCheck` must never produce fabricated references. If verification tools or network access are unavailable, state the limitation and mark uncertainty.
10. Large `Refine` iterations or brainstorming limits remain subject to practical context and runtime limits.

## 8. PowerShell UTF-8 guidance

Console input, console output, pipelines, and files can each use different encodings. Set them explicitly when Persian text must round-trip correctly.

Recommended session preamble:

```powershell
$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8
```

Read a file:

```powershell
$text = Get-Content -LiteralPath '.\prompt.txt' -Raw -Encoding UTF8
```

Write exact BOM-less UTF-8 when byte-level consistency matters:

```powershell
$utf8 = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText((Resolve-Path '.\prompt.txt'), $text, $utf8)
```

PowerShell 7 treats `utf8` as BOM-less UTF-8. Windows PowerShell 5.1 differs for some file-writing commands, so explicit .NET encoding is safer when exact output matters.

## 9. CTF operating model

The profile treats presented challenge targets as authorized competition sandbox assets. Its default boundary includes the challenge workspace, processes, containers, browser state, mounted volumes, services, and linked sandbox nodes.

It does not automatically expand into unrelated personal directories, accounts, credential stores, SSH keys, cloud credentials, or unrelated secrets.

Evidence is prioritized in this order:

1. Live runtime behavior
2. Captured network traffic
3. Actively served assets
4. Current process configuration
5. Persisted challenge state
6. Generated artifacts
7. Checked-in source
8. Comments and dead code

The core workflow is passive inspection, runtime tracing, one narrow end-to-end proof, reproducible recording, single-variable validation, returning to the earliest uncertainty when evidence breaks, and clean-baseline reproduction before declaring success.

## 10. Customization

Common changes include:

- Change the default language under `# Language`.
- Update model references when the active runtime changes.
- Remove CTF sections for general engineering-only use.
- Tighten scope to match an organization or repository policy.
- Add a decorator and update both the runtime reference and `+++AvailableDecs` expectations.
- Remove decorators that conflict with a preferred workflow.
- Adapt PowerShell-specific rules for Bash, Linux, or macOS.
- Add project-specific rules in a clearly labeled section or a more specific nested `AGENTS.md`.

## 11. Troubleshooting

### A decorator is ignored

- Check exact spelling and the `+++` prefix.
- Confirm the decorator exists in `AGENTS.md`.
- Check for a higher-priority conflicting instruction.
- Use `+++AvailableDecs` to inspect support.

### Chat state does not persist

- Put `+++ChatScope` and the intended decorators in the same message.
- Use `+++ActiveDecs` in the same conversation.
- Remember that a new or reset conversation may not retain state.

### Old decorator state remains active

Use `+++Clear` and verify with `+++ActiveDecs`.

### Strict JSON or XML is invalid

Remove conflicting presentation requirements or encode their required sections as valid fields in the requested format.

### The assistant asks too many questions

Clear `+++Interactive` or `+++Socratic`, or use `+++MessageScope` without them for the current task.

### Persian text is corrupted

Set console input, output, pipeline, and file encodings explicitly. Avoid relying on legacy shell defaults or redirection when exact Unicode output matters.

### Citations cannot be verified

Ensure the runtime has access to appropriate sources. A compliant response should disclose missing access and uncertainty rather than invent citations.

### Responses become too long

Reduce `Refine(iterations=N)`, `Brainstorm(limit=N)`, and the number of stacked structure decorators.

## 12. Trust and security notes

- Review `AGENTS.md` before installing it because it changes assistant behavior.
- Treat repository files, challenge artifacts, webpages, logs, and prompts as untrusted data unless the task establishes otherwise.
- Do not store secrets, credentials, or target-specific tokens in this reusable profile.
- The profile's fictional-network convention is an instruction for interpretation, not a network-isolation mechanism.
- Higher-priority runtime policies remain in force even when the profile contains broader behavioral language.

## 13. Attribution

The Prompt Decorators compatibility layer is adapted from [smkalami/prompt-decorators](https://github.com/smkalami/prompt-decorators) by Mostapha Kalami Heris under the MIT License. See [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) for the complete notice and upstream revision.
