---
name: fieldops-powershell-utf8
description: Write, review, and repair PowerShell that must preserve Persian/Farsi or other Unicode across console input, console output, native-process pipelines, and file I/O. Use for mojibake, BOM requirements, multilingual automation, or PowerShell 5.1 versus 7 compatibility. Do not trigger when encoding is irrelevant.
---

# PowerShell UTF-8

Start Unicode-sensitive sessions explicitly:

```powershell
$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8
```

Read with `Get-Content -LiteralPath ... -Raw -Encoding UTF8`. For exact BOM-less writes, use `[System.IO.File]::WriteAllText($path, $text, $utf8)`. Avoid legacy redirection defaults.

Read `references/encoding-matrix.md` for cross-version/BOM work. Run `scripts/test-utf8-roundtrip.ps1` to validate deterministic file encoding. The script is ASCII-only so Windows PowerShell 5.1 cannot corrupt its source literals. Treat console rendering and native-process pipes as separate boundaries and test them separately when the task depends on them.
