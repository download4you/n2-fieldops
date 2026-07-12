import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "fieldops-ctf-operator" / "scripts" / "route_challenge.py"
ROUTED = {
    "fieldops-ctf-ai-ml", "fieldops-ctf-crypto", "fieldops-ctf-forensics",
    "fieldops-ctf-malware", "fieldops-ctf-misc", "fieldops-ctf-osint",
    "fieldops-ctf-pwn", "fieldops-ctf-reverse", "fieldops-ctf-web",
}


def route(*args: str):
    process = subprocess.run([sys.executable, str(ROUTER), "--json", *args], capture_output=True, text=True, encoding="utf-8")
    return process, json.loads(process.stdout) if process.returncode == 0 else None


class CtfRouterTests(unittest.TestCase):
    def test_representative_descriptions(self):
        cases = {
            "RSA modulus with partial prime leak": "fieldops-ctf-crypto",
            "HTTP JWT authentication bypass": "fieldops-ctf-web",
            "LoRA adapter prompt injection": "fieldops-ctf-ai-ml",
            "PCAP packet capture with deleted file transfer": "fieldops-ctf-forensics",
            "C2 beacon configuration extraction": "fieldops-ctf-malware",
            "restricted eval pyjail encoding puzzle": "fieldops-ctf-misc",
        }
        for description, expected in cases.items():
            with self.subTest(description=description):
                process, result = route(description)
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(result["primary"], expected)

    def test_native_binary_routing_and_no_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            binary = Path(temporary) / "challenge.elf"
            binary.write_bytes(b"\x7fELF" + b"\x00" * 64)
            before = hashlib.sha256(binary.read_bytes()).digest(), binary.stat().st_mtime_ns
            process, result = route("--path", str(binary))
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(result["primary"], "fieldops-ctf-reverse")
            self.assertEqual(before, (hashlib.sha256(binary.read_bytes()).digest(), binary.stat().st_mtime_ns))
            _, exploit = route("--path", str(binary), "remote service crashes on long input")
            self.assertEqual(exploit["primary"], "fieldops-ctf-pwn")
            self.assertIn("fieldops-ctf-reverse", exploit["secondary"])

    def test_unknown_fallback_is_deterministic(self):
        first_process, first = route()
        second_process, second = route()
        self.assertEqual(first_process.returncode, second_process.returncode, 0)
        self.assertEqual(first, second)
        self.assertEqual(first["primary"], "fieldops-ctf-misc")
        self.assertEqual(first["confidence"], "low")
        self.assertTrue(first["fallback"])

    def test_invalid_path_exits_two(self):
        process = subprocess.run([sys.executable, str(ROUTER), "--path", str(ROOT / "missing-artifact")], capture_output=True, text=True)
        self.assertEqual(process.returncode, 2)

    def test_schema_and_routed_directories(self):
        _, result = route("HTTP JWT authentication bypass")
        self.assertEqual(set(result), {"primary", "confidence", "scores", "signals", "secondary", "mixed", "fallback"})
        self.assertIn(result["primary"], ROUTED)
        self.assertNotIn("fieldops-ctf-writeup", result["scores"])
        self.assertIn("fieldops-ctf-crypto", result["secondary"])
        for name in ROUTED:
            self.assertTrue((ROOT / name / "SKILL.md").is_file())

    def test_router_uses_standard_library_only(self):
        source = ROUTER.read_text(encoding="utf-8")
        allowed = {"argparse", "json", "os", "re", "sys", "collections", "pathlib", "__future__"}
        imports = set()
        for line in source.splitlines():
            if line.startswith("import "):
                imports.add(line.split()[1].split(".")[0])
            elif line.startswith("from "):
                imports.add(line.split()[1].split(".")[0])
        self.assertLessEqual(imports, allowed)


if __name__ == "__main__":
    unittest.main()
