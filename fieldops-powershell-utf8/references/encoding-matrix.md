# Encoding Matrix

| Boundary | PowerShell 7 | Windows PowerShell 5.1 | Reliable choice |
|---|---|---|---|
| `.ps1` source | UTF-8 without BOM is supported | BOM-less UTF-8 is decoded with the legacy ANSI code page | Use UTF-8 BOM for non-ASCII 5.1 scripts, or keep source ASCII-only |
| UTF-8 file writes | `utf8` is normally BOM-less | `-Encoding UTF8` normally writes a BOM | Use .NET `UTF8Encoding($false/$true)` for exact bytes |
| Console input/output | Host-dependent | Legacy code pages are common | Set both `[Console]` encodings explicitly |
| Object pipeline | .NET objects, not encoded bytes | .NET objects, not encoded bytes | Encoding applies only when crossing a text/byte boundary |
| Native-process stdin/stdout | Tool and host dependent | Legacy defaults are common | Set `$OutputEncoding`; configure or verify the native tool |
| Redirection/`Out-File` | Defaults differ by command | Often UTF-16LE or legacy behavior | Prefer explicit cmdlet encoding or .NET file APIs |
| JSON/CSV | Cmdlet/version differences remain | Compatibility differences are larger | Serialize, then write with an explicit encoding |

Never infer correct Unicode from exit code `0` or from comparing two strings that may
have been corrupted by the same source-decoding error. Compare independent expected
UTF-8 bytes, Base64, hashes, or Unicode code points.
