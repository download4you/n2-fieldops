# Decorator Catalog

Names are case-sensitive. Unknown names remain literal text. Invalid parameters leave
that decorator inactive; valid decorators in the same message still apply.

| Name | Parameters | Kind | Effect |
|---|---|---|---|
| Reasoning | none | behavior | Visible rationale, assumptions, and evidence |
| StepByStep | none | behavior | Labeled ordered steps |
| Socratic | none | behavior | Clarify and explore when questions materially help |
| Debate | none | behavior | Compare, rebut, and conclude |
| Critique | none | behavior | Strengths, weaknesses, and improvements |
| Refine | `iterations=1..5` | behavior | Iterative improvement |
| CiteSources | none | behavior | Credible available citations |
| FactCheck | none | behavior | Verify and qualify material claims |
| OutputFormat | `format=NONEMPTY` | behavior | Strict output container |
| Tone | `style=TEXT<=80` | behavior | Presentation style |
| ChatScope | none | scope | Persist following behavioral decorators |
| MessageScope | none | scope | Pause stored state for this response; apply following decorators once |
| Clear | optional supported names | state | Clear all or selected retained state |
| ActiveDecs | none | inspection | Report retained active state |
| AvailableDecs | none | inspection | Report support and retained status |
| Interactive | `limit=1..5`, `style=brief|detailed` | behavior | Ask only materially blocking questions |
| Planning | none | behavior | Plan then execute |
| Brainstorm | `limit=1..20`, `diversity=low|medium|high` | behavior | Generate options without early judgment |
| Rewrite | none | behavior | Rewrite then answer |
| Import | `topic=TEXT<=80` | behavior | Apply a conceptual lens |
| Candor | `level=low|medium|high` | behavior | Feedback directness |
| Export | `format=text|markdown|json|yaml` | command | Self-contained visible conversation export |
| Dump | same as Export | command | Raw/quick Export alias |

`ActiveDecs` returns exactly `No active decorators` when retained state is empty.
`AvailableDecs` uses the columns `Name`, `Description`, and `Status`.
