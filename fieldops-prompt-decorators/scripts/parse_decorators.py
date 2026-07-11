#!/usr/bin/env python3
"""Parse FieldOps Prompt Decorators without executing them."""

from __future__ import annotations

import argparse
import json
import re
import sys

SUPPORTED = {
    "Reasoning", "StepByStep", "Socratic", "Debate", "Critique", "Refine",
    "CiteSources", "FactCheck", "OutputFormat", "Tone", "ChatScope",
    "MessageScope", "Clear", "ActiveDecs", "AvailableDecs", "Interactive",
    "Planning", "Brainstorm", "Rewrite", "Import", "Candor", "Export", "Dump",
}

TOKEN = re.compile(r"(?<!\\)\+\+\+([A-Za-z][A-Za-z0-9]*)(?:\(([^\n()]*)\))?")


def visible_text(text: str) -> str:
    result: list[str] = []
    fenced = False
    for line in text.splitlines(keepends=True):
        if re.match(r"^\s*```", line):
            fenced = not fenced
            result.append("\n" if line.endswith("\n") else "")
            continue
        if fenced or re.match(r"^\s*>", line):
            result.append("\n" if line.endswith("\n") else "")
            continue
        line = re.sub(r"`[^`\n]*`", "", line)
        stripped = line.strip()
        if len(stripped) >= 2 and stripped[0] in {'"', "'"} and stripped[-1] == stripped[0]:
            result.append("\n" if line.endswith("\n") else "")
            continue
        result.append(line)
    return "".join(result)


def split_parts(raw: str) -> tuple[list[str], list[str]]:
    if not raw.strip():
        return [], []
    parts, current, quote, escaped = [], [], None, False
    for char in raw:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif quote:
            if char == quote:
                quote = None
            else:
                current.append(char)
        elif char in {'"', "'"}:
            quote = char
        elif char == ",":
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    parts.append("".join(current).strip())
    errors = []
    if quote or escaped:
        errors.append("unterminated quote or escape")
    return parts, errors


def key_value_params(parts: list[str], errors: list[str]) -> tuple[dict[str, str], list[str]]:
    params: dict[str, str] = {}
    for part in parts:
        if "=" not in part:
            errors.append(f"invalid parameter: {part}")
            continue
        key, value = (item.strip() for item in part.split("=", 1))
        if not key or not value:
            errors.append(f"invalid parameter: {part}")
        else:
            params[key] = value
    return params, errors


def integer_param(params: dict[str, str], key: str, low: int, high: int, errors: list[str]) -> None:
    if key not in params:
        return
    try:
        value = int(params[key])
    except ValueError:
        errors.append(f"{key} must be an integer")
        return
    if not low <= value <= high:
        errors.append(f"{key} must be between {low} and {high}")


def validate_params(name: str, raw: str) -> tuple[dict[str, object], list[str]]:
    parts, errors = split_parts(raw)
    if name == "Clear":
        targets = [part.removeprefix("+++").strip() for part in parts if part.strip()]
        for target in targets:
            if target not in SUPPORTED:
                errors.append(f"unknown clear target: {target}")
        return ({"targets": targets} if targets else {}), errors

    params, errors = key_value_params(parts, errors)
    no_params = {
        "Reasoning", "StepByStep", "Socratic", "Debate", "Critique",
        "CiteSources", "FactCheck", "ChatScope", "MessageScope", "ActiveDecs",
        "AvailableDecs", "Planning", "Rewrite",
    }
    if name in no_params and params:
        errors.append("this decorator does not accept parameters")
        return params, errors

    allowed = {
        "Refine": {"iterations"},
        "OutputFormat": {"format"},
        "Tone": {"style"},
        "Interactive": {"limit", "style"},
        "Brainstorm": {"limit", "diversity"},
        "Import": {"topic"},
        "Candor": {"level"},
        "Export": {"format"},
        "Dump": {"format"},
    }.get(name, set())
    for key in params:
        if key not in allowed:
            errors.append(f"unknown parameter: {key}")

    if name == "Refine":
        if "iterations" not in params:
            errors.append("missing parameter: iterations")
        integer_param(params, "iterations", 1, 5, errors)
    elif name == "Interactive":
        params.setdefault("limit", "3")
        params.setdefault("style", "brief")
        integer_param(params, "limit", 1, 5, errors)
        if params["style"] not in {"brief", "detailed"}:
            errors.append("style must be brief or detailed")
    elif name == "Brainstorm":
        params.setdefault("limit", "8")
        params.setdefault("diversity", "medium")
        integer_param(params, "limit", 1, 20, errors)
        if params["diversity"] not in {"low", "medium", "high"}:
            errors.append("diversity must be low, medium, or high")
    elif name == "Candor" and params.get("level") not in {"low", "medium", "high"}:
        errors.append("level must be low, medium, or high")
    elif name in {"Export", "Dump"} and params.get("format") not in {"text", "markdown", "json", "yaml"}:
        errors.append("format must be text, markdown, json, or yaml")
    elif name in {"OutputFormat", "Tone", "Import"}:
        key = {"OutputFormat": "format", "Tone": "style", "Import": "topic"}[name]
        value = params.get(key, "")
        if not value:
            errors.append(f"missing parameter: {key}")
        elif name in {"Tone", "Import"} and len(value) > 80:
            errors.append(f"{key} must be at most 80 characters")
    return params, errors


def parse(text: str) -> dict[str, object]:
    scan = visible_text(text)
    tokens = []
    for match in TOKEN.finditer(scan):
        name, raw_params = match.group(1), match.group(2) or ""
        params, errors = validate_params(name, raw_params)
        if name not in SUPPORTED:
            errors.append("unknown decorator")
        tokens.append({
            "name": name,
            "raw": match.group(0),
            "parameters": params,
            "valid": not errors,
            "errors": errors,
            "offset": match.start(),
        })
    return {"tokens": tokens, "count": len(tokens)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", help="UTF-8 prompt file; stdin when omitted")
    args = parser.parse_args()
    text = open(args.path, encoding="utf-8").read() if args.path else sys.stdin.read()
    json.dump(parse(text), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
