from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


SKILLS = (
    "fieldops-ctf-ai-ml",
    "fieldops-ctf-crypto",
    "fieldops-ctf-forensics",
    "fieldops-ctf-malware",
    "fieldops-ctf-misc",
    "fieldops-ctf-osint",
    "fieldops-ctf-pwn",
    "fieldops-ctf-reverse",
    "fieldops-ctf-web",
)
TEXT_EXTENSIONS = {
    ".c", ".cpp", ".css", ".go", ".html", ".ini", ".java", ".js", ".json",
    ".log", ".md", ".php", ".ps1", ".py", ".rb", ".rs", ".sh", ".toml",
    ".ts", ".txt", ".xml", ".yaml", ".yml",
}
EXTENSIONS = {
    "fieldops-ctf-forensics": {".pcap": 10, ".pcapng": 10, ".raw": 5, ".mem": 8, ".dmp": 8, ".ad1": 9, ".e01": 9, ".evtx": 9, ".vmdk": 8, ".wav": 4},
    "fieldops-ctf-reverse": {".exe": 6, ".dll": 6, ".elf": 8, ".so": 6, ".apk": 9, ".wasm": 9, ".dex": 8, ".bin": 4, ".uf2": 7},
    "fieldops-ctf-malware": {".vbs": 5, ".hta": 6, ".ps1": 3, ".docm": 7, ".xlsm": 7},
    "fieldops-ctf-ai-ml": {".onnx": 9, ".pt": 8, ".pth": 8, ".safetensors": 9, ".ckpt": 8, ".h5": 7},
    "fieldops-ctf-web": {".php": 4, ".html": 3, ".js": 2, ".ts": 2},
}
KEYWORDS = {
    "fieldops-ctf-web": ((r"\bhttps?\b|\bhttp\b|\bapi\b|jwt|oauth|saml|cookie|session|ssti|ssrf|xxe|xss|sql.?injection|template|request smuggling|prototype pollution", 4),),
    "fieldops-ctf-pwn": ((r"buffer overflow|format string|ret2libc|\brop\b|shellcode|heap exploit|use.after.free|double free|seccomp|remote service|crash(?:es|ed)? on|memory corruption", 5),),
    "fieldops-ctf-crypto": (
        (r"\brsa\b|\baes\b|\becc\b|cipher|signature|modulus|prime leak|padding oracle|nonce|prng|lattice|\blwe\b|coppersmith|hash collision|length extension", 5),
        (r"\bjwt\b|custom mac", 2),
    ),
    "fieldops-ctf-reverse": ((r"reverse engineer|disassembl|decompil|firmware|bytecode|custom vm|packed binary|crackme|\bwasm\b|\bapk\b|native binary", 5),),
    "fieldops-ctf-forensics": ((r"pcap|packet capture|disk image|memory dump|volatility|registry|event log|stegan|file carving|deleted file|spectrogram|dtmf", 5),),
    "fieldops-ctf-malware": ((r"malware|ransomware|\bc2\b|command.and.control|persistence|beacon|implant|malicious package|yara|process injection|config extraction", 5),),
    "fieldops-ctf-osint": ((r"osint|geolocat|social media|username enumeration|public records|wayback|reverse image|dns records|attribution", 5),),
    "fieldops-ctf-ai-ml": ((r"machine learning|neural network|adversarial example|model extraction|prompt injection|membership inference|training data|\blora\b|checkpoint|safetensors", 5),),
    "fieldops-ctf-misc": ((r"pyjail|bash jail|restricted (?:eval|shell|interpreter)|esoteric|brainfuck|encoding puzzle|\bsdr\b|radio frequency|qr code|game theory", 5),),
}


def iter_paths(path: Path):
    if path.is_file():
        yield path
        return
    for root, dirs, files in os.walk(path, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not (Path(root) / d).is_symlink())
        for name in sorted(files):
            candidate = Path(root) / name
            if not candidate.is_symlink():
                yield candidate


def add_signal(scores, signals, skill: str, source: str, value: str, weight: int) -> None:
    scores[skill] += weight
    signals.append({"skill": skill, "source": source, "value": value, "weight": weight})


def classify(texts: list[str], paths: list[Path]) -> dict[str, object]:
    scores: dict[str, int] = defaultdict(int)
    signals: list[dict[str, object]] = []
    combined_parts = list(texts)
    native = False

    for supplied in paths:
        for index, candidate in enumerate(iter_paths(supplied)):
            if index >= 512:
                break
            suffix = candidate.suffix.lower()
            combined_parts.append(candidate.name)
            for skill, extensions in EXTENSIONS.items():
                if suffix in extensions:
                    add_signal(scores, signals, skill, "extension", suffix, extensions[suffix])
            try:
                prefix = candidate.read_bytes()[:65536]
            except OSError:
                continue
            if prefix.startswith(b"\x7fELF") or prefix.startswith(b"MZ"):
                native = True
                add_signal(scores, signals, "fieldops-ctf-reverse", "signature", "native executable", 7)
            if suffix in TEXT_EXTENSIONS:
                combined_parts.append(prefix.decode("utf-8", errors="replace"))

    combined = "\n".join(combined_parts).lower()
    for skill, rules in KEYWORDS.items():
        for pattern, weight in rules:
            matches = sorted(set(re.findall(pattern, combined, flags=re.I)))
            for match in matches[:3]:
                value = match if isinstance(match, str) else " ".join(match)
                add_signal(scores, signals, skill, "keyword", value, weight)

    exploit_context = bool(re.search(r"remote service|crash(?:es|ed)? on|buffer overflow|format string|memory corruption|\brop\b", combined))
    if native and exploit_context:
        add_signal(scores, signals, "fieldops-ctf-pwn", "combination", "native executable plus exploit behavior", 10)
        add_signal(scores, signals, "fieldops-ctf-reverse", "secondary", "binary understanding supports exploitation", 2)

    ranked = sorted(SKILLS, key=lambda skill: (-scores[skill], skill))
    fallback = scores[ranked[0]] <= 0
    if fallback:
        primary = "fieldops-ctf-misc"
        confidence = "low"
        secondary: list[str] = []
    else:
        primary = ranked[0]
        lead = scores[ranked[0]] - scores[ranked[1]]
        confidence = "high" if scores[ranked[0]] >= 8 and lead >= 4 else "medium" if scores[ranked[0]] >= 4 and lead >= 2 else "low"
        secondary = [skill for skill in ranked[1:] if scores[skill] > 0][:3]
    mixed = bool(secondary and scores[secondary[0]] >= max(3, scores[primary] - 3))
    ordered_scores = {skill: scores[skill] for skill in ranked if scores[skill] > 0}
    ordered_signals = sorted(signals, key=lambda item: (-int(item["weight"]), str(item["skill"]), str(item["value"])))
    return {
        "primary": primary,
        "confidence": confidence,
        "scores": ordered_scores,
        "signals": ordered_signals,
        "secondary": secondary,
        "mixed": mixed,
        "fallback": fallback,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministically route an authorized CTF challenge to a bundled FieldOps specialist.")
    parser.add_argument("text", nargs="*", help="Challenge description or service observations")
    parser.add_argument("--path", action="append", default=[], help="Supplied challenge file or directory")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = [Path(value).resolve() for value in args.path]
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        print(f"error: inaccessible path: {missing[0]}", file=sys.stderr)
        return 2
    result = classify(args.text, paths)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=False))
    else:
        print(f"Primary: {result['primary']} ({result['confidence']} confidence)")
        if result["secondary"]:
            print("Secondary: " + ", ".join(result["secondary"]))
        for signal in result["signals"][:8]:
            print(f"- {signal['source']}: {signal['value']} -> {signal['skill']} (+{signal['weight']})")
        if result["fallback"]:
            print("Fallback classification: begin passive inspection and update the hypothesis from observed evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
