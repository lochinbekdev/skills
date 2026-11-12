# Findings quality: confidence, challenge, and machine export (shared)

Scanners are valued for deterministic, auditable, low-false-positive output. These skills
match that by scoring confidence, challenging every finding, and emitting a machine-readable
export alongside the Markdown report.

## Severity and confidence are separate axes
Give every finding BOTH:
- **Severity** — `critical` / `high` / `medium` / `low` / `info`, from demonstrated impact and a
  CWE/CVE where one applies. Never raise severity on theory alone.
- **Confidence** — `confirmed` / `likely` / `unconfirmed` (below). A high-severity `unconfirmed`
  finding is still reported, labelled honestly, with what is needed to confirm it.

## Confidence & challenge (low false positives)
Every finding carries an explicit **confidence**: `confirmed` (independently reproduced),
`likely` (strong evidence, not reproduced), or `unconfirmed` (static/inference only).
- Before reporting, **challenge** the finding: state what would make it a false positive and
  rule it out with evidence. An unchallenged finding stays `unconfirmed`.
- `confirmed` requires the independent reproduction in `report-standard.md` (fresh
  session, verified role/tenant, matched control, rollback). `HTTP 200` is never enough.
- Separate **observed impact** from **theoretical impact**; never upgrade severity on theory.

## Determinism & reproducibility
- Give every finding a **stable ID** (`SA-001`) and every test/evidence a stable ID, so two
  runs can be diffed and a finding tracked across re-audits.
- Record the exact request/response, actor identity, and changed factor for each result, so
  anyone can replay it. Coverage is a matrix (reviewed/tested/n-a/not-tested), not a sample.

## Machine-readable export (CI & tooling)
The machine-readable export is **off by default** — produce it only when the user asks or when
running in CI, and agree its path first (it is a second written file under the write boundary).
When it is produced, emit a findings file so results gate pipelines and feed dashboards:
- Prefer **SARIF 2.1.0** (`*.sarif`) — rule id, level, message, location, and a partial
  fingerprint from the stable finding ID. Fall back to a documented JSON array.
- Keep it in sync with the Markdown findings; the Markdown stays the human source of truth.
- This export is a permitted deliverable **only** when the user agrees its path, under the
  same write-boundary rules as the report.

## CI / non-interactive mode
When scope, environment, and accounts are supplied up front (config/flags/env), **skip the
intake interview** (`intake.md` phases 2–4) and run directly, then emit the SARIF/JSON
plus a short summary with counts by severity and confidence. Still never perform destructive,
enumerating, or out-of-scope actions.
