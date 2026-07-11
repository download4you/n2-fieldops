[CmdletBinding()]
param([string]$Path = (Join-Path $env:TEMP 'fieldops-utf8-test.txt'))

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

# ASCII-only source: construct Persian, em dash, and emoji from code points.
$codePoints = @(0x0641, 0x0627, 0x0631, 0x0633, 0x06CC)
$persian = -join ($codePoints | ForEach-Object { [char]$_ })
$sample = $persian + ' ' + [char]0x2014 + ' English ' + [char]0x2014 + ' ' + [char]::ConvertFromUtf32(0x1F600)
$expectedBytes = $utf8.GetBytes($sample)

[System.IO.File]::WriteAllBytes($Path, $expectedBytes)
$actualBytes = [System.IO.File]::ReadAllBytes($Path)
$actualText = $utf8.GetString($actualBytes)

$bytesMatch = [System.Linq.Enumerable]::SequenceEqual([byte[]]$expectedBytes, [byte[]]$actualBytes)
$textMatch = $actualText -ceq $sample
$bomPresent = $actualBytes.Length -ge 3 -and $actualBytes[0] -eq 0xEF -and $actualBytes[1] -eq 0xBB -and $actualBytes[2] -eq 0xBF

if (-not $bytesMatch -or -not $textMatch -or $bomPresent) {
    throw "UTF-8 validation failed: $Path"
}

[pscustomobject]@{
    Path = $Path
    PowerShellVersion = $PSVersionTable.PSVersion.ToString()
    Edition = $PSVersionTable.PSEdition
    InputEncoding = [Console]::InputEncoding.WebName
    OutputEncoding = [Console]::OutputEncoding.WebName
    PipelineEncoding = $OutputEncoding.WebName
    ExpectedBase64 = [Convert]::ToBase64String($expectedBytes)
    ActualBase64 = [Convert]::ToBase64String($actualBytes)
    BomPresent = $bomPresent
    BytesMatch = $bytesMatch
    TextMatch = $textMatch
    Passed = $true
}
