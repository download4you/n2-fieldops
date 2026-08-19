# Meta-Decorators

Meta-decorators activate a predefined stack of behavioral decorators at chat scope.
When a meta-decorator is validated, treat `+++ChatScope` as active first, then apply
the stack below. Each member behaves exactly as defined in `decorator-catalog.md`.
Deactivation clears the meta-decorator and every member it activated.

## `+++N2`

Meta-decorator for deep, rigorous analysis. Auto-activates in order: `+++ChatScope`,
`+++Reasoning`, `+++StepByStep`, `+++FactCheck`, `+++Refine(iterations=3)`.

**Structure:** [Activate] → [Reasoning] → [Step-by-Step] → [Fact-Check] → [Refinements] → [Final Answer].

**Rules:**

- Acknowledge active decorators in one compact line every response.
- Label every technical claim — verified evidence / inferred conclusion / speculation
  (especially malware, reverse-engineering, and CTF work).
- Conflicting evidence → present both, weigh, state which you trust and why.
- Each refinement states what changed (evidence added, assumption corrected,
  conclusion tightened).
- Final answer = the most concise version satisfying all prior steps.
- Invoked outside chat scope → treat `+++ChatScope` as active first.
- Deactivate: `+++Clear(+++N2, +++Reasoning, +++StepByStep, +++FactCheck, +++Refine, +++ChatScope)`,
  or `+++MessageScope` for one message.

**Parameter:** `iterations` (integer 1..5, default 3) — `+++N2(iterations=5)` → 5 passes.

**Use:** complex malware triage, multi-stage reverse engineering, crypto analysis —
anywhere a wrong conclusion is costly.

## `+++Storm`

Meta-decorator for genuinely novel ideas — raw generation + lateral reframing +
adversarial pressure. Auto-activates in order: `+++ChatScope`,
`+++Brainstorm(limit=15, diversity=high)`, `+++Import(topic="Lateral Thinking")`,
`+++Debate`, `+++Refine(iterations=3)`, `+++Critique`.

**Structure:** [Activate] → [Novelty Scan: what exists] → [Raw Brainstorm: cross-domain analogs] → [Lateral Lens] → [Debate: steelman + counter each] → [Iter 1: dedupe + cluster] → [Iter 2: strengthen with mechanism] → [Iter 3: rank Novelty × Feasibility × Impact] → [Critique: kill derivatives] → [Final List].

**Rules:**

- Acknowledge active decorators every response.
- Novelty Scan mandatory first (existing tools, techniques, papers, malware families,
  research — to avoid duplicating).
- Brainstorm unfiltered, deliberately cross-domain (biology, physics, game theory,
  economics, social systems, hardware, ML, linguistics).
- Debate: strongest attack + defense per idea; keep survivors.
- Iter 1: drop duplicates and "X but for Y" with no new mechanism.
- Iter 2: each survivor states a mechanism not publicly documented in the obvious
  place (label speculation).
- Iter 3: rank; state criteria.
- Critique kills: minor variations of known techniques, no plausible mechanism, not
  statable in one sentence without jargon stacking, duplicates of anything publicly
  findable in 5 minutes.
- Final list: 3–7 ideas, each with one-line summary, mechanism, why-not-public (or
  why the public version is incomplete), risk, next concrete step.
- End with mandatory paragraph "Why this is new: …" (one sentence per idea — what
  makes it different, or admit known technique + new twist).
- Invoked outside chat scope → treat `+++ChatScope` as active first.
- Deactivate: `+++Clear(+++Storm, +++ChatScope, +++Brainstorm, +++Import, +++Debate, +++Refine, +++Critique)`.

**Parameters:** `limit` (integer 1..20, default 15) raw ideas · `diversity`
(low | medium | high; default high — high forces cross-domain, medium stays adjacent)
· `iterations` (integer 1..5, default 3) · `lens` (string ≤ 80 chars, default
"Lateral Thinking"; also First Principles, Biological Analogs, Game Theory,
Adversarial ML, Hardware Constraints, Economic Incentives, Evolutionary Pressure,
Information Theory, Complexity Theory) · `domain` (string ≤ 80 chars, optional)
binds brainstorm to one field, e.g. `+++Storm(domain="malware persistence")`;
default unbounded.

**Uses:** novel persistence, EDR evasion, C2 channels (incl. non-network), detection
for unknown families, YARA structures, ML training data, memory forensics, unpacking,
deobfuscation, supply-chain surfaces, identity vectors, legitimate stego channels,
sandbox-escape testing.
