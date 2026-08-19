import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_SKILLS = {
    "fieldops-orchestrator",
    "fieldops-research",
    "fieldops-prompt-decorators",
    "fieldops-ctf-operator",
    "fieldops-engineering",
    "fieldops-powershell-utf8",
    "fieldops-prompt-refiner",
}
BUNDLED_CTF_SKILLS = {
    "fieldops-ctf-ai-ml",
    "fieldops-ctf-crypto",
    "fieldops-ctf-forensics",
    "fieldops-ctf-malware",
    "fieldops-ctf-misc",
    "fieldops-ctf-osint",
    "fieldops-ctf-pwn",
    "fieldops-ctf-reverse",
    "fieldops-ctf-web",
    "fieldops-ctf-writeup",
}
SKILLS = CORE_SKILLS | BUNDLED_CTF_SKILLS
UPSTREAM_URL = "https://github.com/ljagiello/ctf-skills"
UPSTREAM_COMMIT = "d19f35fd3dd2e126108752aee84c657c888126d3"
TECHNIQUE_FILES = {
    "fieldops-ctf-ai-ml": {"adversarial-ml.md", "llm-attacks.md", "model-attacks.md"},
    "fieldops-ctf-crypto": {"advanced-math.md", "classic-ciphers.md", "ecc-attacks.md", "exotic-crypto.md", "exotic-crypto-2.md", "historical.md", "lattice-and-lwe.md", "modern-ciphers.md", "modern-ciphers-2.md", "modern-ciphers-3.md", "prng.md", "prng-attacks.md", "rsa-attacks.md", "rsa-attacks-2.md", "stream-ciphers.md", "zkp-and-advanced.md"},
    "fieldops-ctf-forensics": {"3d-printing.md", "disk-advanced.md", "disk-and-memory.md", "disk-recovery.md", "linux-forensics.md", "network.md", "network-advanced.md", "peripheral-capture.md", "signals-and-hardware.md", "steganography.md", "stego-advanced.md", "stego-advanced-2.md", "stego-image.md", "windows.md"},
    "fieldops-ctf-malware": {"c2-and-protocols.md", "pe-and-dotnet.md", "scripts-and-obfuscation.md"},
    "fieldops-ctf-misc": {"bashjails.md", "ctfd-navigation.md", "dns.md", "encodings.md", "encodings-advanced.md", "games-and-vms.md", "games-and-vms-2.md", "games-and-vms-3.md", "games-and-vms-4.md", "linux-privesc.md", "pyjails.md", "rf-sdr.md"},
    "fieldops-ctf-osint": {"geolocation-and-media.md", "social-media.md", "web-and-dns.md"},
    "fieldops-ctf-pwn": {"advanced.md", "advanced-exploits.md", "advanced-exploits-2.md", "advanced-exploits-3.md", "advanced-exploits-4.md", "advanced-exploits-5.md", "field-notes.md", "format-string.md", "heap-fsop.md", "heap-techniques.md", "heap-techniques-2.md", "kernel.md", "kernel-bypass.md", "kernel-techniques.md", "overflow-basics.md", "rop-advanced.md", "rop-and-shellcode.md", "sandbox-escape.md"},
    "fieldops-ctf-reverse": {"anti-analysis.md", "anti-analysis-ctf.md", "field-notes.md", "languages.md", "languages-compiled.md", "languages-platforms.md", "patterns.md", "patterns-ctf.md", "patterns-ctf-2.md", "patterns-ctf-3.md", "patterns-runtime.md", "platforms.md", "platforms-hardware.md", "tools.md", "tools-advanced.md", "tools-advanced-2.md", "tools-dynamic.md", "tools-emulation.md"},
    "fieldops-ctf-web": {"auth-and-access.md", "auth-and-access-2.md", "auth-infra.md", "auth-jwt.md", "client-side.md", "client-side-advanced.md", "cves.md", "field-notes.md", "node-and-prototype.md", "server-side.md", "server-side-2.md", "server-side-advanced.md", "server-side-advanced-2.md", "server-side-advanced-3.md", "server-side-advanced-4.md", "server-side-deser.md", "server-side-exec.md", "server-side-exec-2.md", "sql-injection.md", "web3.md"},
    "fieldops-ctf-writeup": set(),
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


def strip_fenced_code(text: str) -> str:
    output = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            output.append("")
        else:
            output.append("" if in_fence else line)
    return "\n".join(output)


def strip_all_code(text: str) -> str:
    return re.sub(r"`[^`]*`", "", strip_fenced_code(text))


def markdown_links(text: str):
    for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", strip_all_code(text)):
        target = match.group(1)
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if "#" in target:
            file_part, anchor = target.split("#", 1)
        else:
            file_part, anchor = target, None
        if file_part.endswith(".md") or (not file_part and anchor):
            yield file_part, anchor


def heading_slugs(text: str) -> set[str]:
    slugs = set()
    for match in re.finditer(r"^#{1,6}\s+(.+)$", strip_fenced_code(text), re.MULTILINE):
        slug = re.sub(r"[*`~]", "", match.group(1).lower().strip())
        slug = re.sub(r"<[^>]+>", "", slug)
        slug = re.sub(r"[^\w\s-]", "", slug).replace(" ", "-")
        slugs.add(slug)
    return slugs


class RepositoryLayoutTests(unittest.TestCase):
    def test_cc_switch_discovers_exactly_17_root_skills(self):
        self.assertFalse((ROOT / "SKILL.md").exists())
        discovered = {path.parent.name for path in ROOT.glob("*/SKILL.md") if path.is_file()}
        self.assertEqual(discovered, SKILLS)
        self.assertEqual(len(discovered), 17)
        nested = []
        for path in ROOT.rglob("SKILL.md"):
            if path.parent.parent != ROOT and ".git" not in path.parts and "dist" not in path.parts:
                nested.append(path)
        self.assertEqual(nested, [], "CC Switch would discover duplicate nested skills")

    def test_release_metadata_is_synchronized(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
        manifest = json.loads(
            (ROOT / "claude-plugin-template" / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads(
            (ROOT / "claude-plugin-template" / "marketplace.template.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["version"], version)
        self.assertEqual(marketplace["version"], version)
        self.assertEqual(marketplace["plugins"][0]["version"], version)
        self.assertTrue((ROOT / "docs" / f"RELEASE_NOTES_{version}.md").is_file())
        self.assertEqual(list((ROOT / "claude-plugin-template").rglob("SKILL.md")), [])

    def test_skill_frontmatter_and_metadata(self):
        for name in SKILLS:
            with self.subTest(skill=name):
                skill_dir = ROOT / name
                skill_path = skill_dir / "SKILL.md"
                raw_frontmatter = re.match(
                    r"\A---\s*\n(.*?)\n---\s*\n",
                    skill_path.read_text(encoding="utf-8"),
                    re.DOTALL,
                ).group(1)
                keys_in_order = [line.split(":", 1)[0].strip() for line in raw_frontmatter.splitlines() if ":" in line]
                self.assertEqual(len(keys_in_order), len(set(keys_in_order)), "duplicate YAML frontmatter key")
                values = frontmatter(skill_path)
                keys = set(values)
                self.assertEqual(keys, {"name", "description"})
                self.assertEqual(values["name"], name)
                self.assertTrue(values["description"])
                metadata = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
                self.assertIn(f"${name}", metadata)

    def test_canonical_skill_prose_is_runtime_neutral(self):
        for name in SKILLS:
            for markdown in (ROOT / name).rglob("*.md"):
                with self.subTest(skill=name, file=markdown.name):
                    self.assertNotIn("$fieldops", markdown.read_text(encoding="utf-8"))

    def test_bundled_ctf_provenance_and_complete_manifest(self):
        reference_license = (ROOT / "fieldops-ctf-ai-ml" / "LICENSE").read_bytes()
        self.assertIn(b"Copyright (c) 2026 Lukasz Jagiello", reference_license)
        for name in BUNDLED_CTF_SKILLS:
            with self.subTest(skill=name):
                skill_dir = ROOT / name
                self.assertEqual((skill_dir / "LICENSE").read_bytes(), reference_license)
                upstream = (skill_dir / "UPSTREAM.md").read_text(encoding="utf-8")
                self.assertIn(UPSTREAM_URL, upstream)
                self.assertIn(UPSTREAM_COMMIT, upstream)
                actual = {path.name for path in skill_dir.glob("*.md")} - {"SKILL.md", "UPSTREAM.md"}
                self.assertEqual(actual, TECHNIQUE_FILES[name])

    def test_skill_resources_are_self_contained(self):
        for name in SKILLS:
            skill_dir = ROOT / name
            for markdown in skill_dir.rglob("*.md"):
                text = markdown.read_text(encoding="utf-8")
                for file_part, _anchor in markdown_links(text):
                    if file_part:
                        target = (markdown.parent / file_part).resolve()
                        self.assertTrue(target.is_relative_to(skill_dir.resolve()), f"cross-skill link: {markdown} -> {file_part}")
                if markdown.name != "UPSTREAM.md":
                    self.assertNotRegex(text, r"/ctf-[\w-]+")
                    self.assertNotIn("solve-challenge", text)
            self.assertFalse((skill_dir / "README.md").exists())
            self.assertFalse((skill_dir / "CHANGELOG.md").exists())

    def test_all_technique_files_are_referenced_by_skill(self):
        for name, filenames in TECHNIQUE_FILES.items():
            skill_text = (ROOT / name / "SKILL.md").read_text(encoding="utf-8")
            for filename in filenames:
                with self.subTest(skill=name, reference=filename):
                    self.assertIn(filename, skill_text)

    def test_relative_markdown_links_and_anchors_resolve(self):
        for markdown in ROOT.rglob("*.md"):
            text = markdown.read_text(encoding="utf-8")
            for file_part, anchor in markdown_links(text):
                target = markdown if not file_part else (markdown.parent / file_part).resolve()
                with self.subTest(file=markdown.relative_to(ROOT), target=f"{file_part}#{anchor or ''}"):
                    self.assertTrue(target.is_file())
                    if anchor:
                        self.assertIn(anchor, heading_slugs(target.read_text(encoding="utf-8")))

    def test_no_changelog_anywhere(self):
        matches = [path for path in ROOT.rglob("*") if "changelog" in path.name.lower()]
        self.assertEqual(matches, [])

    def test_root_notice_contains_pinned_upstream_license(self):
        notice = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
        self.assertIn(UPSTREAM_URL, notice)
        self.assertIn(UPSTREAM_COMMIT, notice)
        self.assertIn("Copyright (c) 2026 Lukasz Jagiello", notice)

    def test_root_prompt_stays_compact_and_portable(self):
        # Relaxed for the current profile. The prompt ships the full CTF Core
        # Contract and cooperation language; the Prompt Decorator reference lives
        # in the fieldops-prompt-decorators skill. The ceiling below still
        # catches accidental bloat (e.g. pasted logs or binaries).
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 500)

    def test_powershell_validation_source_is_ascii(self):
        path = ROOT / "fieldops-powershell-utf8" / "scripts" / "test-utf8-roundtrip.ps1"
        path.read_bytes().decode("ascii")


if __name__ == "__main__":
    unittest.main()
