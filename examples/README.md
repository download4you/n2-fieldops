# Copy-Ready Examples

## Route an unfamiliar task

```text
Use $fieldops-orchestrator to classify this task, select the smallest useful set of
FieldOps skills, execute it, and verify the result.
```

## Research a current or disputed claim

```text
Use $fieldops-research to verify the important claims, distinguish fact from
inference, and give me a direct recommendation with sources and a next step.
```

## Solve an authorized challenge

```text
Use $fieldops-ctf-operator to classify this authorized CTF challenge, preserve the
original artifacts, prove one decisive path, and reproduce the solution.
```

## One-message technical plan

```text
+++MessageScope
+++Planning
+++StepByStep
+++Tone(style=technical)

Plan and implement a safe database migration.
```

## Persistent review mode

```text
+++ChatScope
+++Critique
+++Candor(level=high)
+++Tone(style=technical)
```

## Strict JSON response

```text
+++MessageScope
+++OutputFormat(format=json)

Return the API risks as objects with id, severity, evidence, and mitigation fields.
```

## Fact-checked research

```text
+++MessageScope
+++FactCheck
+++CiteSources
+++OutputFormat(format=markdown)

Verify the claims in this proposal and cite authoritative sources.
```

## High-diversity brainstorming

```text
+++MessageScope
+++Brainstorm(limit=8, diversity=high)

Generate deployment options for an intermittently connected edge system.
```

## Apply a systems lens

```text
+++MessageScope
+++Import(topic="Systems Thinking")
+++Debate

Should this platform move from a monolith to microservices?
```

## Rewrite and improve a request

```text
+++MessageScope
+++Rewrite
+++Refine(iterations=3)

make the api better and secure
```

## Conversation handoff

```text
+++MessageScope
+++Export(format=markdown)

Export the current task state, decisions, open questions, changed files, and active decorators.
```

## Inspect and reset state

```text
+++ActiveDecs
```

```text
+++Clear
```
