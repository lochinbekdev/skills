#!/usr/bin/env python3
"""Check a findings export against the shape docs/findings-quality.md asks for.

    python3 scripts/validate-sarif.py path/to/findings.sarif

Not a full SARIF 2.1.0 schema validation: it checks the fields these skills promise, and
that nothing that looks like a credential slipped into the file.
"""
from __future__ import annotations

import json
import re
import sys

ID_RE = re.compile(r"^(SA|AUTHN|AC|API|UP|DEP|MS|RT)-\d{3,}$")
LEVELS = {"error", "warning", "note", "none"}
CONFIDENCE = {"confirmed", "likely", "unconfirmed"}
SECRET_RE = re.compile(
    r"(eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.|Bearer\s+[A-Za-z0-9._-]{20,}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----|\bpassword\s*[:=]\s*\S{6,})",
    re.I,
)


def main(path: str) -> int:
    problems: list[str] = []
    raw = open(path, encoding="utf-8").read()
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"✗ not valid JSON: {e}")
        return 1

    if doc.get("version") != "2.1.0":
        problems.append(f"version is {doc.get('version')!r}, expected '2.1.0'")
    runs = doc.get("runs") or []
    if not runs:
        problems.append("no runs")

    total = 0
    for ri, run in enumerate(runs):
        driver = (run.get("tool") or {}).get("driver") or {}
        if not driver.get("name"):
            problems.append(f"runs[{ri}].tool.driver.name missing")
        rule_ids = {r.get("id") for r in driver.get("rules") or []}
        for i, res in enumerate(run.get("results") or []):
            total += 1
            where = f"runs[{ri}].results[{i}]"
            rid = res.get("ruleId", "")
            if not ID_RE.match(rid):
                problems.append(f"{where}: ruleId {rid!r} is not a stable finding ID (e.g. AC-001)")
            if rid not in rule_ids:
                problems.append(f"{where}: ruleId {rid!r} has no entry in tool.driver.rules")
            if res.get("level") not in LEVELS:
                problems.append(f"{where}: level {res.get('level')!r} not one of {sorted(LEVELS)}")
            if not (res.get("message") or {}).get("text"):
                problems.append(f"{where}: message.text missing")
            if (res.get("partialFingerprints") or {}).get("findingId/v1") != rid:
                problems.append(f"{where}: partialFingerprints['findingId/v1'] must equal ruleId")
            conf = (res.get("properties") or {}).get("confidence")
            if conf not in CONFIDENCE:
                problems.append(f"{where}: properties.confidence {conf!r} not one of {sorted(CONFIDENCE)}")
            for li, loc in enumerate(res.get("locations") or []):
                uri = ((loc.get("physicalLocation") or {}).get("artifactLocation") or {}).get("uri", "")
                if uri.startswith("/") or re.match(r"^[A-Za-z]:\\", uri):
                    problems.append(f"{where}.locations[{li}]: uri {uri!r} must be relative to the audited root")

    m = SECRET_RE.search(raw)
    if m:
        problems.append(f"something that looks like a credential is in the file: {m.group(0)[:24]}…")

    if problems:
        print(f"✗ {len(problems)} problem(s) in {path}:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"✓ {path}: {total} finding(s), shape OK")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
