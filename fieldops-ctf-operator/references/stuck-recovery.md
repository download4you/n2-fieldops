# Stuck recovery

Treat the investigation as stuck after two attempts that produce no discriminating evidence, a failed clean reproduction, or a conflict between runtime and source evidence.

1. State the exact claim currently being tested.
2. Separate verified facts from assumptions.
3. Identify the earliest unsupported assumption.
4. Choose one test whose outcomes distinguish at least two hypotheses.
5. Change category when the blocker belongs to another domain.
6. Change tool family when repeated tools share the same blind spot.
7. Inspect alternate layers: transport, encoding, wrapper, loader, storage, cache, worker, or generated artifact.
8. Check simpler paths: logic flaw, default state, metadata, stale artifact, alternate endpoint, or unintended parser behavior.
9. Record negative evidence and do not repeat equivalent attempts.
10. After finding a candidate solution, reset and replay only the minimal chain.

## Common pivots

- Web client blob or WASM -> `fieldops-ctf-reverse`
- JWT or custom signature -> `fieldops-ctf-crypto`
- Binary understood but exploit primitive needed -> `fieldops-ctf-pwn`
- PCAP contains an executable or C2 -> `fieldops-ctf-malware`
- Dump reveals an identity or location clue -> `fieldops-ctf-osint`
- Unknown encoding or restricted interpreter -> `fieldops-ctf-misc`
- Model artifact or prompt boundary -> `fieldops-ctf-ai-ml`
