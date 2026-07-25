---
name: fieldops-powershell-utf8
description: Writes, reviews, and repairs PowerShell so Persian/Farsi and other Unicode text survives console input, console output, native-process pipelines, and file I/O. Use when text turns into mojibake or question-mark boxes, when a UTF-8 BOM must be added or removed, for multilingual or non-ASCII automation, or when a script behaves differently under Windows PowerShell 5.1 versus PowerShell 7. Trigger keywords include mojibake, garbled/broken characters, UTF-8, BOM, encoding, chcp/code page, Get-Content/Out-File/Set-Content encoding, and Persian/Farsi/Unicode output. Skip when encoding is irrelevant.
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
