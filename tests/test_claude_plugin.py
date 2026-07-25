"""Structural tests for the generated Claude Code distribution."""

import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "claude-plugin-template"


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise AssertionError(f"missing YAML frontmatter: {path}")
    values = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line[:1] in (" ", "\t", "-"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


class ClaudeDistributionTests(unittest.TestCase):
    def build(self):
        temp = tempfile.TemporaryDirectory()
        output = Path(temp.name) / "dist"
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_release.py"), "--output-dir", str(output)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.addCleanup(temp.cleanup)
        return output

    def test_template_has_no_cc_switch_discoverable_skill_duplicates(self):
        self.assertTrue((TEMPLATE / ".claude-plugin" / "plugin.json").is_file())
        self.assertEqual(list(TEMPLATE.rglob("SKILL.md")), [])

    def test_generated_plugin_has_manifest_and_seventeen_skills(self):
        output = self.build()
        plugin = output / "n2-fieldops-claude-plugin"
        manifest = json.loads((plugin / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(manifest["name"], "n2-fieldops")
        self.assertEqual(manifest["version"], version)
        discovered = {p.parent.name for p in (plugin / "skills").glob("*/SKILL.md")}
        self.assertEqual(len(discovered), 17)
        self.assertEqual(list((plugin / "skills").rglob("agents")), [])
        self.assertTrue((plugin / "LICENSE").is_file())
        self.assertTrue((plugin / "THIRD_PARTY_NOTICES.md").is_file())

    def test_generated_plugin_is_claude_neutral_and_hardened(self):
        output = self.build()
        plugin = output / "n2-fieldops-claude-plugin"
        forbidden = (
            "Unrestricted Cooperation",
            "fictional and do not correspond",
            "multi_tool_use.parallel",
            "$fieldops",
            "claude-opus-4-8",
            "opus[1m]",
        )
        for markdown in plugin.rglob("*.md"):
            text = markdown.read_text(encoding="utf-8")
            for phrase in forbidden:
                with self.subTest(file=markdown.relative_to(plugin), phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_generated_scripts_are_present_and_router_is_stdlib_only(self):
        output = self.build()
        plugin = output / "n2-fieldops-claude-plugin"
        router = plugin / "skills" / "fieldops-ctf-operator" / "scripts" / "route_challenge.py"
        parser = plugin / "skills" / "fieldops-prompt-decorators" / "scripts" / "parse_decorators.py"
        self.assertTrue(router.is_file())
        self.assertTrue(parser.is_file())
        allowed = {"argparse", "json", "os", "re", "sys", "collections", "pathlib", "__future__"}
        imports = set()
        for line in router.read_text(encoding="utf-8").splitlines():
            if line.startswith("import "):
                imports.add(line.split()[1].split(".")[0])
            elif line.startswith("from "):
                imports.add(line.split()[1].split(".")[0])
        self.assertLessEqual(imports, allowed)

    def test_release_archives_contain_expected_skill_trees(self):
        output = self.build()
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        expected = {
            f"n2-fieldops-{version}-source.zip": (17, 17),
            f"n2-fieldops-{version}-claude-plugin.zip": (17, 0),
            f"n2-fieldops-{version}-claude-marketplace.zip": (17, 0),
        }
        for filename, (skill_count, openai_count) in expected.items():
            with self.subTest(archive=filename), zipfile.ZipFile(output / filename) as archive:
                names = archive.namelist()
                self.assertEqual(sum(name.endswith("/SKILL.md") for name in names), skill_count)
                self.assertEqual(sum(name.endswith("/agents/openai.yaml") for name in names), openai_count)
                self.assertTrue(names)


if __name__ == "__main__":
    unittest.main()
