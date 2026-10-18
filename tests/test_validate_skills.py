import unittest
from pathlib import Path
import tempfile
import shutil
import sys

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate_skills import (
    validate_skill_file,
    validate_agent_file,
    validate_repository,
    Issue,
    Severity,
    estimate_token_count,
)

class TestValidateSkills(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.root_path = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_estimate_token_count(self):
        text = "word " * 10
        # 10 words, approx 13-15 tokens
        tokens = estimate_token_count(text)
        self.assertGreater(tokens, 0)
        self.assertLessEqual(tokens, 20)

    def test_validate_valid_skill(self):
        skill_dir = self.root_path / ".agents" / "skills" / "test-skill"
        skill_dir.mkdir(parents=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            "---\n"
            "name: test-skill\n"
            "description: Validates testing operations.\n"
            "---\n\n"
            "# Test Skill\n"
            "Some content here.\n"
        )
        issues, stats = validate_skill_file(skill_file, self.root_path)
        errors = [i for i in issues if i.severity == Severity.ERROR]
        self.assertEqual(len(errors), 0)
        self.assertEqual(stats["name"], "test-skill")

    def test_validate_skill_missing_frontmatter(self):
        skill_dir = self.root_path / ".agents" / "skills" / "bad-skill"
        skill_dir.mkdir(parents=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text("# Bad Skill\nNo frontmatter at all.\n")

        issues, stats = validate_skill_file(skill_file, self.root_path)
        errors = [i for i in issues if i.severity == Severity.ERROR]
        self.assertTrue(any("frontmatter" in e.message.lower() for e in errors))
        # Ensure remediation guide is present on error
        self.assertTrue(any(e.guidance is not None for e in errors))

    def test_validate_skill_deprecated_syntax(self):
        skill_dir = self.root_path / ".agents" / "skills" / "vendor-skill"
        skill_dir.mkdir(parents=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            "---\n"
            "name: vendor-skill\n"
            "description: Uses vendor tags.\n"
            "---\n\n"
            "Here is some vendor syntax: <thinking>internal thought</thinking>\n"
        )
        issues, _ = validate_skill_file(skill_file, self.root_path)
        warnings = [i for i in issues if i.severity == Severity.WARNING]
        self.assertTrue(any("vendor" in w.message.lower() or "thinking" in w.message.lower() for w in warnings))

    def test_validate_broken_relative_links(self):
        skill_dir = self.root_path / ".agents" / "skills" / "link-skill"
        skill_dir.mkdir(parents=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            "---\n"
            "name: link-skill\n"
            "description: Checks links.\n"
            "---\n\n"
            "Read [missing.md](missing.md) and [http link](https://google.com).\n"
        )
        issues, _ = validate_skill_file(skill_file, self.root_path)
        errors = [i for i in issues if i.severity == Severity.ERROR]
        self.assertTrue(any("missing.md" in e.message for e in errors))

    def test_validate_valid_agent(self):
        agent_dir = self.root_path / ".agents" / "agents" / "test-agent"
        agent_dir.mkdir(parents=True)
        agent_file = agent_dir / "agent.md"
        agent_file.write_text(
            "---\n"
            "name: test-agent\n"
            "description: Test agent description.\n"
            "tools:\n"
            "  - view_file\n"
            "subagent: true\n"
            "model: inherit\n"
            "---\n\n"
            "# Role\nTest agent role.\n"
        )
        issues, stats = validate_agent_file(agent_file, self.root_path)
        errors = [i for i in issues if i.severity == Severity.ERROR]
        self.assertEqual(len(errors), 0)
        self.assertEqual(stats["name"], "test-agent")

    def test_validate_agent_missing_fields(self):
        agent_dir = self.root_path / ".agents" / "agents" / "incomplete-agent"
        agent_dir.mkdir(parents=True)
        agent_file = agent_dir / "agent.md"
        agent_file.write_text(
            "---\n"
            "name: incomplete-agent\n"
            "---\n\n"
            "# Role\nMissing description, tools, subagent.\n"
        )
        issues, _ = validate_agent_file(agent_file, self.root_path)
        errors = [i for i in issues if i.severity == Severity.ERROR]
        self.assertTrue(len(errors) >= 2)
        # Verify developer guidance exists
        self.assertTrue(all(e.guidance for e in errors))

if __name__ == "__main__":
    unittest.main()
