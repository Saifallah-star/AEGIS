#!/usr/bin/env python3
"""
Antigravity Skill & Subagent Quality Verification Tool
Validates YAML frontmatter, context token weight, vendor-specific syntax,
and link integrity with short developer remediation guides.
"""

import sys
import re
import argparse
from pathlib import Path
from enum import Enum
from typing import List, Dict, Tuple, Optional, Any
import yaml

class Severity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class Issue:
    def __init__(
        self,
        severity: Severity,
        file_path: Path,
        message: str,
        guidance: Optional[str] = None,
        line_num: Optional[int] = None,
    ):
        self.severity = severity
        self.file_path = file_path
        self.message = message
        self.guidance = guidance
        self.line_num = line_num

    def __repr__(self):
        return f"[{self.severity.value}] {self.file_path}: {self.message}"

# ANSI Colors
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_CYAN = "\033[96m"
COLOR_BOLD = "\033[1m"
COLOR_DIM = "\033[2m"

# Deprecated vendor artifacts regexes
VENDOR_PATTERNS = [
    (r"<thinking>", "Found '<thinking>' Claude-specific XML tag.", "Antigravity agents do not use Claude XML thinking tags. Remove <thinking> tags."),
    (r"</thinking>", "Found '</thinking>' Claude-specific XML tag.", "Remove </thinking> tags."),
    (r"<function_calls>", "Found Claude-style '<function_calls>' tag.", "Use native Antigravity tool calling conventions instead."),
    (r"@claude", "Found '@claude' mention.", "Antigravity agents run on Gemini/agy. Update vendor mentions."),
    (r"@openai", "Found '@openai' mention.", "Antigravity agents run on Gemini/agy. Update vendor mentions."),
]

def estimate_token_count(text: str) -> int:
    """
    Estimates token count using the standard approximation: ~4 characters per token
    or ~0.75 tokens per word for English prose.
    """
    if not text:
        return 0
    words = len(text.split())
    chars = len(text)
    # Balanced heuristic
    return int((words * 1.3 + chars / 4.0) / 2)

def extract_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], Optional[str], Optional[str]]:
    """
    Extracts YAML frontmatter and body.
    Returns: (parsed_yaml, raw_frontmatter, body)
    """
    if not content.startswith("---"):
        return None, None, content
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, None, content
    
    raw_fm = parts[1]
    body = parts[2]
    
    try:
        parsed = yaml.safe_load(raw_fm)
        if isinstance(parsed, dict):
            return parsed, raw_fm, body
        return None, raw_fm, body
    except yaml.YAMLError as exc:
        return None, raw_fm, str(exc)

def check_relative_links(file_path: Path, body: str, root_dir: Path) -> List[Issue]:
    """
    Scans markdown body for relative file links and ensures targets exist.
    """
    issues = []
    # Markdown link pattern: [label](url)
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    file_dir = file_path.parent

    for match in link_pattern.finditer(body):
        label, url = match.groups()
        # Skip external web URLs, anchors, mailto, etc.
        if url.startswith(("http://", "https://", "mailto:", "#", "file://", "conversation://")):
            continue
        
        # Remove anchor if present: file.md#heading
        target_path_str = url.split("#")[0]
        if not target_path_str:
            continue
        
        # Resolve target
        if target_path_str.startswith("/"):
            target_file = root_dir / target_path_str.lstrip("/")
        else:
            target_file = (file_dir / target_path_str).resolve()
        
        if not target_file.exists():
            issues.append(
                Issue(
                    severity=Severity.ERROR,
                    file_path=file_path,
                    message=f"Broken relative markdown link '{url}' (target does not exist on disk).",
                    guidance=f"Check that target file '{target_path_str}' exists relative to '{file_dir.relative_to(root_dir)}' or correct the path.",
                )
            )
    return issues

def check_vendor_syntax(file_path: Path, content: str) -> List[Issue]:
    """
    Checks for deprecated vendor-specific syntax or XML prompts.
    """
    issues = []
    for pattern, msg, guide in VENDOR_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(
                Issue(
                    severity=Severity.WARNING,
                    file_path=file_path,
                    message=msg,
                    guidance=guide,
                )
            )
    return issues

def validate_skill_file(skill_file: Path, root_dir: Path) -> Tuple[List[Issue], Dict[str, Any]]:
    """
    Validates a SKILL.md file against Antigravity requirements.
    """
    issues: List[Issue] = []
    stats: Dict[str, Any] = {
        "name": None,
        "char_count": 0,
        "token_est": 0,
        "body_lines": 0,
    }

    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as exc:
        issues.append(
            Issue(
                severity=Severity.ERROR,
                file_path=skill_file,
                message=f"Could not read skill file: {exc}",
                guidance="Ensure the file has read permissions and valid UTF-8 encoding.",
            )
        )
        return issues, stats

    stats["body_lines"] = len(content.splitlines())

    fm, raw_fm, body = extract_frontmatter(content)
    if fm is None:
        issues.append(
            Issue(
                severity=Severity.ERROR,
                file_path=skill_file,
                message="Missing or invalid YAML frontmatter in SKILL.md.",
                guidance="Every SKILL.md must start with '---', contain 'name' and 'description', and close with '---'.",
            )
        )
        return issues, stats

    # Validate 'name'
    name = fm.get("name")
    if not name or not isinstance(name, str):
        issues.append(
            Issue(
                severity=Severity.ERROR,
                file_path=skill_file,
                message="Missing or invalid 'name' in YAML frontmatter.",
                guidance="Add 'name: <skill-name>' matching the parent directory name.",
            )
        )
    else:
        stats["name"] = name
        parent_name = skill_file.parent.name
        if name != parent_name:
            issues.append(
                Issue(
                    severity=Severity.WARNING,
                    file_path=skill_file,
                    message=f"Skill name '{name}' does not match parent folder '{parent_name}'.",
                    guidance=f"Change frontmatter name to '{parent_name}' for consistent indexing.",
                )
            )

    # Validate 'description'
    desc = fm.get("description")
    if not desc or not isinstance(desc, str):
        issues.append(
            Issue(
                severity=Severity.ERROR,
                file_path=skill_file,
                message="Missing or invalid 'description' in YAML frontmatter.",
                guidance="Add a 3rd-person description explaining what the skill does and when to activate it.",
            )
        )
    else:
        char_count = len(desc.strip())
        token_est = estimate_token_count(desc.strip())
        stats["char_count"] = char_count
        stats["token_est"] = token_est

        if char_count < 20:
            issues.append(
                Issue(
                    severity=Severity.WARNING,
                    file_path=skill_file,
                    message=f"Skill description is very short ({char_count} chars).",
                    guidance="Elaborate on trigger keywords and use cases to improve autonomous model selection.",
                )
            )
        elif char_count > 600:
            issues.append(
                Issue(
                    severity=Severity.WARNING,
                    file_path=skill_file,
                    message=f"Skill description is quite long ({char_count} chars, ~{token_est} tokens).",
                    guidance="Keep progressive disclosure descriptions concise (under 500 chars) to conserve index context tokens.",
                )
            )

    # Check vendor syntax
    issues.extend(check_vendor_syntax(skill_file, content))

    # Check relative links
    if body:
        issues.extend(check_relative_links(skill_file, body, root_dir))

    return issues, stats

def validate_agent_file(agent_file: Path, root_dir: Path) -> Tuple[List[Issue], Dict[str, Any]]:
    """
    Validates an agent.md definition.
    """
    issues: List[Issue] = []
    stats: Dict[str, Any] = {
        "name": None,
        "tools_count": 0,
        "skills_count": 0,
    }

    try:
        content = agent_file.read_text(encoding="utf-8")
    except Exception as exc:
        issues.append(
            Issue(
                severity=Severity.ERROR,
                file_path=agent_file,
                message=f"Could not read agent file: {exc}",
                guidance="Ensure the file has read permissions and valid UTF-8 encoding.",
            )
        )
        return issues, stats

    fm, raw_fm, body = extract_frontmatter(content)
    if fm is None:
        issues.append(
            Issue(
                severity=Severity.ERROR,
                file_path=agent_file,
                message="Missing or invalid YAML frontmatter in agent.md.",
                guidance="Agent definitions require YAML frontmatter specifying 'name', 'description', 'tools', and 'subagent: true'.",
            )
        )
        return issues, stats

    # Validate name
    name = fm.get("name")
    if not name or not isinstance(name, str):
        issues.append(
            Issue(
                severity=Severity.ERROR,
                file_path=agent_file,
                message="Missing 'name' in agent YAML frontmatter.",
                guidance="Specify 'name: <agent-name>' matching the agent folder.",
            )
        )
    else:
        stats["name"] = name

    # Validate description
    desc = fm.get("description")
    if not desc or not isinstance(desc, str):
        issues.append(
            Issue(
                severity=Severity.ERROR,
                file_path=agent_file,
                message="Missing 'description' in agent YAML frontmatter.",
                guidance="Add a concise description explaining the agent's role and when to dispatch it.",
            )
        )

    # Validate tools
    tools = fm.get("tools")
    if tools is None:
        issues.append(
            Issue(
                severity=Severity.ERROR,
                file_path=agent_file,
                message="Missing 'tools' list in agent frontmatter.",
                guidance="Specify allowed tools (e.g., view_file, grep_search, replace_file_content, run_command).",
            )
        )
    elif not isinstance(tools, list):
        issues.append(
            Issue(
                severity=Severity.ERROR,
                file_path=agent_file,
                message="'tools' must be a YAML list of tool names.",
                guidance="Format tools as a YAML list: 'tools: [view_file, grep_search]'.",
            )
        )
    else:
        stats["tools_count"] = len(tools)

    # Validate subagent flag
    if not fm.get("subagent"):
        issues.append(
            Issue(
                severity=Severity.WARNING,
                file_path=agent_file,
                message="Missing 'subagent: true' in agent frontmatter.",
                guidance="Set 'subagent: true' so Antigravity marks this agent definition as an autonomous worker.",
            )
        )

    # Validate skills binding if present
    skills = fm.get("skills")
    if skills:
        if isinstance(skills, list):
            stats["skills_count"] = len(skills)
            for skill_ref in skills:
                # e.g. skills/tdd or .agents/skills/tdd
                norm_ref = skill_ref.replace(".agents/", "").replace("skills/", "")
                skill_target = root_dir / ".agents" / "skills" / norm_ref / "SKILL.md"
                if not skill_target.exists():
                    issues.append(
                        Issue(
                            severity=Severity.WARNING,
                            file_path=agent_file,
                            message=f"Bound skill '{skill_ref}' not found at '{skill_target.relative_to(root_dir)}'.",
                            guidance=f"Check that skill folder '.agents/skills/{norm_ref}' exists or update the reference.",
                        )
                    )
        else:
            issues.append(
                Issue(
                    severity=Severity.ERROR,
                    file_path=agent_file,
                    message="'skills' must be a list of skill references.",
                    guidance="Format bound skills as a list: 'skills: [skills/tdd]'.",
                )
            )

    issues.extend(check_vendor_syntax(agent_file, content))
    if body:
        issues.extend(check_relative_links(agent_file, body, root_dir))

    return issues, stats

def validate_repository(root_dir: Path) -> Tuple[List[Issue], Dict[str, Any]]:
    """
    Validates all skills and subagents in the repository.
    """
    all_issues: List[Issue] = []
    repo_stats: Dict[str, Any] = {
        "skills_checked": 0,
        "agents_checked": 0,
        "total_tokens_est": 0,
        "skills_data": [],
        "agents_data": [],
    }

    skills_dir = root_dir / ".agents" / "skills"
    if skills_dir.exists():
        for skill_path in sorted(skills_dir.glob("*/SKILL.md")):
            issues, stats = validate_skill_file(skill_path, root_dir)
            all_issues.extend(issues)
            repo_stats["skills_checked"] += 1
            repo_stats["total_tokens_est"] += stats.get("token_est", 0)
            repo_stats["skills_data"].append((skill_path, stats, issues))

    agents_dir = root_dir / ".agents" / "agents"
    if agents_dir.exists():
        for agent_path in sorted(agents_dir.glob("*/agent.md")):
            issues, stats = validate_agent_file(agent_path, root_dir)
            all_issues.extend(issues)
            repo_stats["agents_checked"] += 1
            repo_stats["agents_data"].append((agent_path, stats, issues))

    return all_issues, repo_stats

def format_terminal_report(all_issues: List[Issue], stats: Dict[str, Any], root_dir: Path) -> str:
    """
    Renders a colored terminal report with summary statistics and remediation guides.
    """
    errors = [i for i in all_issues if i.severity == Severity.ERROR]
    warnings = [i for i in all_issues if i.severity == Severity.WARNING]

    lines = []
    lines.append("")
    lines.append(f"{COLOR_BOLD}{COLOR_CYAN}======================================================================{COLOR_RESET}")
    lines.append(f"{COLOR_BOLD}{COLOR_CYAN}       Antigravity Skill & Agent Quality Verification Report           {COLOR_RESET}")
    lines.append(f"{COLOR_BOLD}{COLOR_CYAN}======================================================================{COLOR_RESET}")
    lines.append("")

    # Summary bar
    lines.append(f"{COLOR_BOLD}Scope:{COLOR_RESET} {stats['skills_checked']} Skills verified | {stats['agents_checked']} Agents verified")
    lines.append(f"{COLOR_BOLD}Context Token Weight:{COLOR_RESET} ~{stats['total_tokens_est']} tokens estimated for progressive disclosure index")
    lines.append("")

    # Skills table
    lines.append(f"{COLOR_BOLD}--- Skills Status ---{COLOR_RESET}")
    lines.append(f"{'Status':<8} {'Skill Name':<28} {'Tokens':<10} {'Path'}")
    lines.append("-" * 70)

    for skill_path, s_stats, issues in stats["skills_data"]:
        s_errs = [i for i in issues if i.severity == Severity.ERROR]
        s_warns = [i for i in issues if i.severity == Severity.WARNING]
        
        rel_path = skill_path.relative_to(root_dir)
        name = s_stats["name"] or skill_path.parent.name

        if s_errs:
            status = f"{COLOR_RED}❌ FAIL{COLOR_RESET}"
        elif s_warns:
            status = f"{COLOR_YELLOW}⚠️ WARN{COLOR_RESET}"
        else:
            status = f"{COLOR_GREEN}✅ PASS{COLOR_RESET}"

        tokens_str = f"~{s_stats['token_est']}"
        lines.append(f"{status:<17} {name:<28} {tokens_str:<10} {rel_path}")

    lines.append("")

    # Agents table
    if stats["agents_data"]:
        lines.append(f"{COLOR_BOLD}--- Subagents Status ---{COLOR_RESET}")
        lines.append(f"{'Status':<8} {'Agent Name':<20} {'Tools':<8} {'Skills':<8} {'Path'}")
        lines.append("-" * 70)
        for agent_path, a_stats, issues in stats["agents_data"]:
            a_errs = [i for i in issues if i.severity == Severity.ERROR]
            a_warns = [i for i in issues if i.severity == Severity.WARNING]

            rel_path = agent_path.relative_to(root_dir)
            name = a_stats["name"] or agent_path.parent.name

            if a_errs:
                status = f"{COLOR_RED}❌ FAIL{COLOR_RESET}"
            elif a_warns:
                status = f"{COLOR_YELLOW}⚠️ WARN{COLOR_RESET}"
            else:
                status = f"{COLOR_GREEN}✅ PASS{COLOR_RESET}"

            tools_str = str(a_stats["tools_count"])
            skills_str = str(a_stats["skills_count"])
            lines.append(f"{status:<17} {name:<20} {tools_str:<8} {skills_str:<8} {rel_path}")
        lines.append("")

    # Remediation Guide Section
    if errors or warnings:
        lines.append(f"{COLOR_BOLD}{COLOR_YELLOW}--- Remediation Guide for Issues Found ---{COLOR_RESET}")
        lines.append("")
        
        idx = 1
        for issue in all_issues:
            if issue.severity == Severity.ERROR:
                badge = f"{COLOR_RED}[ERROR]{COLOR_RESET}"
            elif issue.severity == Severity.WARNING:
                badge = f"{COLOR_YELLOW}[WARNING]{COLOR_RESET}"
            else:
                badge = f"{COLOR_BLUE}[INFO]{COLOR_RESET}"

            rel_file = issue.file_path.relative_to(root_dir)
            lines.append(f"{idx}. {badge} {COLOR_BOLD}{rel_file}{COLOR_RESET}")
            lines.append(f"   {COLOR_DIM}Problem:{COLOR_RESET} {issue.message}")
            if issue.guidance:
                lines.append(f"   {COLOR_CYAN}Fix Guide:{COLOR_RESET} {issue.guidance}")
            lines.append("")
            idx += 1

    # Final verdict
    lines.append("=" * 70)
    if errors:
        lines.append(f"{COLOR_BOLD}{COLOR_RED}VERDICT: FAILED ({len(errors)} error(s), {len(warnings)} warning(s)){COLOR_RESET}")
    elif warnings:
        lines.append(f"{COLOR_BOLD}{COLOR_YELLOW}VERDICT: PASSED WITH WARNINGS (0 errors, {len(warnings)} warning(s)){COLOR_RESET}")
    else:
        lines.append(f"{COLOR_BOLD}{COLOR_GREEN}VERDICT: ALL CHECKS PASSED PERFECTLY (0 errors, 0 warnings){COLOR_RESET}")
    lines.append("=" * 70)
    lines.append("")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Antigravity Skill & Subagent Quality Verification Tool")
    parser.add_argument("--root", type=str, default=".", help="Root directory of the repository")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings as well as errors")
    args = parser.parse_args()

    root_dir = Path(args.root).resolve()
    issues, stats = validate_repository(root_dir)
    report = format_terminal_report(issues, stats, root_dir)
    print(report)

    errors = [i for i in issues if i.severity == Severity.ERROR]
    warnings = [i for i in issues if i.severity == Severity.WARNING]

    if errors:
        sys.exit(1)
    if args.strict and warnings:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
