import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "fieldops-orchestrator",
    "fieldops-research",
    "fieldops-prompt-decorators",
    "fieldops-ctf-operator",
    "fieldops-engineering",
    "fieldops-powershell-utf8",
    "fieldops-prompt-refiner",
}


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise AssertionError(f"Missing YAML frontmatter: {path}")
    values = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


class RepositoryLayoutTests(unittest.TestCase):
    def test_cc_switch_discovers_expected_root_skills(self):
        discovered = {
            path.parent.name for path in ROOT.glob("*/SKILL.md") if path.is_file()
        }
        self.assertEqual(discovered, SKILLS)

    def test_skill_frontmatter_and_metadata(self):
        for name in SKILLS:
            with self.subTest(skill=name):
                skill_dir = ROOT / name
                values = frontmatter(skill_dir / "SKILL.md")
                self.assertEqual(set(values), {"name", "description"})
                self.assertEqual(values["name"], name)
                self.assertTrue(values["description"])
                metadata = (skill_dir / "agents" / "openai.yaml").read_text(
                    encoding="utf-8"
                )
                self.assertIn(f"${name}", metadata)

    def test_skill_resources_are_self_contained(self):
        for name in SKILLS:
            with self.subTest(skill=name):
                skill_dir = ROOT / name
                text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
                self.assertNotIn("../", text)
                for relative in re.findall(r"`((?:references|scripts)/[^`]+)`", text):
                    self.assertTrue((skill_dir / relative).is_file(), relative)
                self.assertFalse((skill_dir / "README.md").exists())
                self.assertFalse((skill_dir / "CHANGELOG.md").exists())

    def test_no_changelog_anywhere(self):
        matches = [path for path in ROOT.rglob("*") if "changelog" in path.name.lower()]
        self.assertEqual(matches, [])

    def test_root_prompt_stays_compact_and_portable(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 220)
        for forbidden in (
            "fictional and do not correspond",
            "Unrestricted Cooperation",
            "multi_tool_use.parallel",
            "detailed explanation of the reasoning and logic",
        ):
            self.assertNotIn(forbidden, text)

    def test_powershell_validation_source_is_ascii(self):
        path = ROOT / "fieldops-powershell-utf8" / "scripts" / "test-utf8-roundtrip.ps1"
        path.read_bytes().decode("ascii")

    def test_relative_markdown_links_resolve(self):
        for markdown in ROOT.rglob("*.md"):
            text = markdown.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                path_text = target.split("#", 1)[0]
                if not path_text:
                    continue
                with self.subTest(file=markdown.relative_to(ROOT), target=target):
                    self.assertTrue((markdown.parent / path_text).resolve().exists())


if __name__ == "__main__":
    unittest.main()
