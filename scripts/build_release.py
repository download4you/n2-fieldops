#!/usr/bin/env python3
"""Build deterministic FieldOps source and native Claude distribution archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import stat
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "claude-plugin-template"
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def read_version() -> str:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not VERSION_RE.fullmatch(version):
        raise ValueError(f"VERSION is not strict semver: {version!r}")
    return version


def root_skills() -> list[Path]:
    skills = sorted(
        path for path in ROOT.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    )
    if len(skills) != 17:
        raise ValueError(f"expected 17 root skills, found {len(skills)}")
    return skills


def validate_layout() -> None:
    expected = {path.name for path in root_skills()}
    for skill_md in ROOT.rglob("SKILL.md"):
        if skill_md.parent.name not in expected or skill_md.parent.parent != ROOT:
            if ".git" not in skill_md.parts and "dist" not in skill_md.parts:
                raise ValueError(
                    "nested SKILL.md would be recursively discovered by CC Switch: "
                    f"{skill_md.relative_to(ROOT)}"
                )
    manifest = TEMPLATE / ".claude-plugin" / "plugin.json"
    if not manifest.is_file():
        raise ValueError(f"missing Claude plugin template manifest: {manifest}")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if data.get("name") != "n2-fieldops":
        raise ValueError("Claude plugin template name must be n2-fieldops")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def transform_for_claude(text: str) -> str:
    # Keep the canonical skill prose portable across Codex and Claude. Claude users
    # should not see Codex-only `$fieldops-*` invocation syntax or repo-relative
    # script paths that cannot resolve from a plugin installation.
    text = re.sub(r"\$fieldops-([a-z0-9-]+)", r"fieldops-\1", text)
    for script in (
        "route_challenge.py",
        "parse_decorators.py",
        "test-utf8-roundtrip.ps1",
    ):
        text = text.replace(
            f"scripts/{script}", f"${{CLAUDE_SKILL_DIR}}/scripts/{script}"
        )
        text = text.replace(
            f"${{CLAUDE_SKILL_DIR}}/${{CLAUDE_SKILL_DIR}}/scripts/{script}",
            f"${{CLAUDE_SKILL_DIR}}/scripts/{script}",
        )
    return text


def copy_skill(source: Path, destination: Path) -> None:
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if "agents" in relative.parts or "__pycache__" in relative.parts:
            continue
        if path.is_file() and path.suffix != ".pyc":
            target = destination / relative
            if path.suffix.lower() in {".md", ".txt", ".yaml", ".yml", ".json", ".py", ".ps1"}:
                write_text(target, transform_for_claude(path.read_text(encoding="utf-8")))
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)


def build_plugin(output: Path, version: str) -> Path:
    plugin = output / "n2-fieldops-claude-plugin"
    plugin.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(
        (TEMPLATE / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    manifest["version"] = version
    write_text(
        plugin / ".claude-plugin" / "plugin.json",
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
    )

    write_text(
        plugin / "README.md",
        (TEMPLATE / "PLUGIN_README.md").read_text(encoding="utf-8"),
    )
    write_text(
        plugin / "LICENSE",
        (TEMPLATE / "LICENSE").read_text(encoding="utf-8"),
    )
    write_text(
        plugin / "THIRD_PARTY_NOTICES.md",
        (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8"),
    )

    docs = plugin / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    for source in sorted((TEMPLATE / "docs").glob("*.md")):
        write_text(docs / source.name, source.read_text(encoding="utf-8"))
    decorator_doc = ROOT / "docs" / "DECORATOR_REFERENCE.md"
    write_text(docs / decorator_doc.name, decorator_doc.read_text(encoding="utf-8"))

    for source in root_skills():
        copy_skill(source, plugin / "skills" / source.name)
    return plugin


def build_marketplace(output: Path, plugin: Path, version: str) -> Path:
    marketplace = output / "n2-fieldops-claude-marketplace"
    target_plugin = marketplace / "plugins" / "n2-fieldops"
    shutil.copytree(plugin, target_plugin)
    template = json.loads(
        (TEMPLATE / "marketplace.template.json").read_text(encoding="utf-8")
    )
    template["version"] = version
    for entry in template.get("plugins", []):
        entry["version"] = version
    write_text(
        marketplace / ".claude-plugin" / "marketplace.json",
        json.dumps(template, indent=2, ensure_ascii=True) + "\n",
    )
    return marketplace


def add_tree(archive: zipfile.ZipFile, source: Path, prefix: str = "") -> None:
    for path in sorted(source.rglob("*")):
        relative_path = path.relative_to(source)
        if (
            not path.is_file()
            or ".git" in relative_path.parts
            or "dist" in relative_path.parts
            or "__pycache__" in relative_path.parts
            or path.suffix == ".pyc"
        ):
            continue
        relative = relative_path.as_posix()
        name = "/".join(part for part in (prefix, relative) if part)
        if name.startswith("/") or ".." in Path(name).parts:
            raise ValueError(f"unsafe archive path: {name}")
        info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = (stat.S_IFREG | 0o644) << 16
        archive.writestr(info, path.read_bytes())


def zip_tree(source: Path, destination: Path, prefix: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        add_tree(archive, source, prefix)


def build_archives(output: Path, version: str, plugin: Path, marketplace: Path) -> list[Path]:
    source_archive = output / f"n2-fieldops-{version}-source.zip"
    plugin_archive = output / f"n2-fieldops-{version}-claude-plugin.zip"
    marketplace_archive = output / f"n2-fieldops-{version}-claude-marketplace.zip"
    zip_tree(ROOT, source_archive, f"n2-fieldops-{version}")
    zip_tree(plugin, plugin_archive, "n2-fieldops-claude-plugin")
    zip_tree(marketplace, marketplace_archive, f"n2-fieldops-claude-marketplace-{version}")
    return [source_archive, plugin_archive, marketplace_archive]


def write_checksums(files: list[Path], output: Path) -> Path:
    lines = []
    for path in sorted(files):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.name}")
    checksums = output / "SHA256SUMS"
    write_text(checksums, "\n".join(lines) + "\n")
    return checksums


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--check", action="store_true", help="validate without writing archives")
    parser.add_argument("--force", action="store_true", help="replace an existing output directory")
    args = parser.parse_args(argv)

    version = read_version()
    validate_layout()
    if args.check:
        print(f"layout and manifests valid for n2-fieldops {version}")
        return 0

    output = args.output_dir.resolve()
    if output.exists() and any(output.iterdir()):
        if not args.force:
            raise SystemExit(f"output directory is not empty: {output} (use --force)")
        for child in output.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    output.mkdir(parents=True, exist_ok=True)
    plugin = build_plugin(output, version)
    marketplace = build_marketplace(output, plugin, version)
    archives = build_archives(output, version, plugin, marketplace)
    checksums = write_checksums(archives, output)
    print(f"built {plugin}")
    print(f"built {marketplace}")
    for path in archives + [checksums]:
        print(path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"build failed: {error}", file=sys.stderr)
        raise SystemExit(2)
