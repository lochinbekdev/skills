#!/usr/bin/env python3
"""Check the things that silently break an installed skill.

Run it before a release, or let CI run it on every push:

    python3 scripts/validate-repo.py

Exits non-zero and prints one line per problem.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills" / "security"
DOCS_DIR = ROOT / "docs"
SHARED_DOCS = [
    "intake.md",
    "write-boundary.md",
    "test-accounts.md",
    "report-standard.md",
    "tooling.md",
    "findings-quality.md",
]
# agentskills.io/specification: lowercase alphanumerics and single hyphens, 1-64 chars.
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

problems: list[str] = []


def fail(where: str, msg: str) -> None:
    problems.append(f"{where}: {msg}")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(path.relative_to(ROOT).as_posix(), "no YAML frontmatter")
        return {}
    end = text.index("\n---", 4)
    out: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def check_skills() -> set[str]:
    names: set[str] = set()
    for skill in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        rel = skill.relative_to(ROOT).as_posix()
        md = skill / "SKILL.md"
        if not md.exists():
            fail(rel, "no SKILL.md")
            continue
        fm = frontmatter(md)
        name = fm.get("name", "")
        names.add(name)
        if name != skill.name:
            fail(rel, f"frontmatter name {name!r} != directory name {skill.name!r}")
        if not NAME_RE.match(name) or len(name) > 64:
            fail(rel, f"name {name!r} is not [a-z0-9] with single hyphens, 1-64 chars")
        if not fm.get("description"):
            fail(rel, "no description")

        yaml_path = skill / "agents" / "openai.yaml"
        if not yaml_path.exists():
            fail(rel, "no agents/openai.yaml")
        else:
            body = yaml_path.read_text(encoding="utf-8")
            m = re.search(r'short_description:\s*"([^"]*)"', body)
            if not m:
                fail(rel, "openai.yaml has no quoted short_description")
            elif not 25 <= len(m.group(1)) <= 64:
                fail(rel, f"openai.yaml short_description is {len(m.group(1))} chars, spec says 25-64")
            p = re.search(r'default_prompt:\s*"([^"]*)"', body)
            if p and f"${name}" not in p.group(1):
                fail(rel, f"openai.yaml default_prompt does not mention ${name}")

        for doc in SHARED_DOCS:
            bundled = skill / "references" / doc
            if not bundled.exists():
                fail(rel, f"references/{doc} missing — run scripts/sync-docs.sh")
            elif bundled.read_bytes() != (DOCS_DIR / doc).read_bytes():
                fail(rel, f"references/{doc} differs from docs/{doc} — run scripts/sync-docs.sh")
    return names


def check_manifests(names: set[str]) -> None:
    claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
    if claude["version"] != codex["version"]:
        fail("manifests", f"version mismatch: Claude {claude['version']}, Codex {codex['version']}")
    if not re.match(r"^\d+\.\d+\.\d+$", codex["version"]):
        fail(".codex-plugin/plugin.json", f"version {codex['version']!r} is not strict semver")

    listed = set()
    for entry in claude.get("skills", []):
        path = ROOT / entry.lstrip("./")
        if not (path / "SKILL.md").exists():
            fail(".claude-plugin/plugin.json", f"skills entry {entry} has no SKILL.md")
        listed.add(path.name)
    missing = names - listed
    if missing:
        fail(".claude-plugin/plugin.json", f"skills not listed: {', '.join(sorted(missing))}")

    codex_skills = ROOT / codex.get("skills", "").lstrip("./")
    if not codex_skills.is_dir():
        fail(".codex-plugin/plugin.json", f"skills path {codex.get('skills')!r} is not a directory")
    for key, where in (("hooks", ".codex-plugin/plugin.json"),):
        if key in codex:
            fail(where, f"{key!r} is rejected by the Codex plugin validator")
    if "[TODO" in json.dumps(codex):
        fail(".codex-plugin/plugin.json", "placeholder text left in the manifest")


def main() -> int:
    names = check_skills()
    check_manifests(names)
    if problems:
        print(f"✗ {len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"✓ {len(names)} skills, manifests and bundled references all consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
