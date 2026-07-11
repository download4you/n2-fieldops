import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARSER = ROOT / "fieldops-prompt-decorators" / "scripts" / "parse_decorators.py"
SPEC = importlib.util.spec_from_file_location("fieldops_parser", PARSER)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class DecoratorParserTests(unittest.TestCase):
    def test_parses_valid_decorators_and_defaults(self):
        result = MODULE.parse("+++Planning\n+++Interactive\nDo the work")
        self.assertEqual([item["name"] for item in result["tokens"]], ["Planning", "Interactive"])
        self.assertEqual(result["tokens"][1]["parameters"], {"limit": "3", "style": "brief"})
        self.assertTrue(all(item["valid"] for item in result["tokens"]))

    def test_ignores_escaped_code_quote_and_blockquote_tokens(self):
        prompt = """\
\\+++Planning
`+++Tone(style=formal)`
"+++FactCheck"
> +++Debate
```text
+++Critique
```
+++Reasoning
"""
        result = MODULE.parse(prompt)
        self.assertEqual([item["name"] for item in result["tokens"]], ["Reasoning"])

    def test_rejects_unknown_and_out_of_range_parameters(self):
        result = MODULE.parse("+++Unknown\n+++Refine(iterations=9)\n+++Candor(level=extreme)")
        self.assertFalse(result["tokens"][0]["valid"])
        self.assertIn("between 1 and 5", " ".join(result["tokens"][1]["errors"]))
        self.assertIn("low, medium, or high", " ".join(result["tokens"][2]["errors"]))

    def test_parses_clear_targets_and_quoted_values(self):
        result = MODULE.parse('+++Clear(+++Tone, +++Planning)\n+++Import(topic="Systems Thinking")')
        self.assertEqual(result["tokens"][0]["parameters"]["targets"], ["Tone", "Planning"])
        self.assertEqual(result["tokens"][1]["parameters"]["topic"], "Systems Thinking")
        self.assertTrue(all(item["valid"] for item in result["tokens"]))


if __name__ == "__main__":
    unittest.main()
