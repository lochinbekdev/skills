# lochinbekdev / skills

Small, composable **security** skills for AI agents, installable as a Claude Code plugin —
like npm/composer/pip, but for agent skills.

Each skill has a **narrow scope**, its own operating rules, and shares three cross-cutting
standards so every audit behaves the same way.

## Install

```
/plugin marketplace add lochinbekdev/skills
/plugin install lochinbekdev-security@lochinbekdev
```

Then run a skill, e.g. `/audit-backend`, or just ask the agent to "audit this backend".

## Skills

| Skill | Scope |
|---|---|
| `audit-backend` | Orchestrator — runs a full, stack-agnostic backend audit and writes the single report. |
| `audit-access-control` | Horizontal / vertical / cross-tenant authorization and field-permission tests with A/B accounts. |
| `audit-api` | Routes, injection, SSRF, CORS, headers, and business-logic abuse. |
| `audit-uploads` | Upload → storage → processing → serving, archive extraction (zip-slip), download authz. |
| `audit-dependencies` | Dependencies, lockfiles, runtime versions, CI/CD, and secret exposure (read-only). |

## Shared standards (`docs/`)

- **`docs/report-standard.md`** — the one deliverable and its fixed structure. Report is written
  in **English by default** (user-selectable), with a mandatory `PARTIAL AUDIT` marker when any practical test
  is incomplete.
- **`docs/test-accounts.md`** — how auth is tested: two lowest-role accounts (A/B), control roles,
  normal login, and matched control/test request pairs.
- **`docs/write-boundary.md`** — the read-only write boundary; the only file written is the report.
- **`docs/intake.md`** — the grill → plan → go protocol: skills recon the project, ask the user for
  missing data as `Q1/Q2…` questions, explain the plan, and start real testing only on an explicit go.

## Principles

- **Authorized only.** A target found in a repo does not authorize testing it.
- **Evidence over status codes.** `HTTP 200` is not proof; every mutation needs a separate read
  and a verified rollback.
- **No harm.** No DoS, brute force, enumeration, RCE, or damage to real data.

## Layout

```
.claude-plugin/
  marketplace.json
  plugin.json
docs/
  intake.md
  report-standard.md
  test-accounts.md
  write-boundary.md
skills/
  security/
    audit-backend/SKILL.md
    audit-access-control/SKILL.md
    audit-api/SKILL.md
    audit-uploads/SKILL.md
    audit-dependencies/SKILL.md
```

## Roadmap

- **Next:** `microservice-interdependency` skill — map inter-service dependencies and produce a
  security report, plus machine-readable export (e.g. SARIF) alongside the Markdown report.
- Repo tooling (versioning, skill validation) once the skill set grows.

## License

MIT — see [LICENSE](./LICENSE).
