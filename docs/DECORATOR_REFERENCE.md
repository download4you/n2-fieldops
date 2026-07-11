# Prompt Decorators Reference

This release defines 23 decorator names. `+++Dump` is an alias of `+++Export`. `+++Validate` is not defined by this profile and is therefore not listed as supported.

| Decorator | Parameters | Required behavior |
|---|---|---|
| `+++Reasoning` | None | Begin with a clear, relevant explanation or rationale. |
| `+++StepByStep` | None | Use labeled steps from `[Step 1]` through `[Final Step]`. |
| `+++Socratic` | None | Restate, clarify definitions, analyze assumptions, explore perspectives, use examples, and encourage inquiry. |
| `+++Debate` | None | State the position, analyze multiple perspectives, rebut, and conclude. |
| `+++Critique` | None | Identify the subject, strengths, weaknesses, improvements, and constructive conclusion. |
| `+++Refine(iterations=N)` | Positive integer `N` | Show iterative improvements followed by a final answer. |
| `+++CiteSources` | None | Support important claims with credible references and full citations. |
| `+++FactCheck` | None | Identify and verify claims, mark uncertainty, and provide verified sources. |
| `+++OutputFormat(format=FORMAT)` | `json`, `markdown`, `yaml`, `xml`, or another clear format | Strictly follow the requested output structure. |
| `+++Tone(style=STYLE)` | Such as `formal`, `casual`, `friendly`, `technical`, or `humorous` | Maintain the requested tone throughout the response. |
| `+++ChatScope` | None | Persist decorators from the same message across later conversation turns. |
| `+++MessageScope` | None | Apply decorators only to the current message and pause stored chat decorators for that message. |
| `+++Clear` | Optional decorator list | Clear all or selected chat-scoped decorators. |
| `+++ActiveDecs` | None | List active chat-scoped decorators or return `No active decorators`. |
| `+++AvailableDecs` | None | Return a Name, Description, Status table for every supported decorator. |
| `+++Interactive(limit=N, style=STYLE)` | Integer limit; `brief` or `detailed` | Identify ambiguity, ask questions, wait, then proceed without inferring missing requirements. |
| `+++Planning` | None | Start with a concise plan, then execute. |
| `+++Brainstorm(limit=N, diversity=LEVEL)` | Integer limit; `low`, `medium`, or `high` | Generate multiple ideas without evaluating them early. |
| `+++Rewrite` | None | Rewrite the user's prompt for clarity, then respond while preserving intent. |
| `+++Import(topic=STRING)` | Named conceptual or disciplinary lens | State the lens, apply it, then answer. |
| `+++Candor(level=LEVEL)` | `low`, `medium`, or `high` | Match feedback directness while remaining professional. |
| `+++Export(format=FORMAT)` | `text`, `markdown`, `json`, or `yaml` | Produce a self-contained conversation export including active decorators when available. |
| `+++Dump` | Same as `+++Export` | Produce a quicker or more raw export using Export behavior. |

## State-control examples

Activate:

```text
+++ChatScope
+++Tone(style=technical)
+++Planning
```

Inspect:

```text
+++ActiveDecs
```

Clear selected decorators:

```text
+++Clear(+++Tone, +++Planning)
```

Clear everything:

```text
+++Clear
```

## Limitations

- Decorators are interpreted by the model and are not executable syntax.
- State persistence depends on retained conversation context.
- Invalid or unsupported parameters have no formal parser-level error contract in the source profile.
- Avoid contradictory scope controllers in one message.
- Higher-priority instructions override decorators.
- Source verification depends on available tools and access.
