# lochinbekdev / skills

Small, composable **security** skills for AI agents, installable as a Claude Code plugin —
like npm/composer/pip, but for agent skills.

Each skill has a **narrow scope**, its own operating rules, and shares three cross-cutting
standards so every audit behaves the same way.

## Install

### Claude Code

```
/plugin marketplace add lochinbekdev/skills
/plugin install lochinbekdev-security@lochinbekdev
```

Then run a skill, e.g. `/audit-backend`, or just ask the agent to "audit this backend".

### OpenAI Codex / other agents

The skills are plain `SKILL.md` instructions, so any agent can use them. Each skill
ships an `agents/openai.yaml` interface descriptor. Link them into your local agent
skill directories (`~/.agents/skills` and `~/.claude/skills`) with:

```
git clone https://github.com/lochinbekdev/skills
cd skills
./scripts/link-skills.sh
```

Each link points back into the repo, so `git pull` keeps the installed skills current.
Codex then discovers them from `~/.agents/skills`. You can also just point your
`AGENTS.md` at a skill's `SKILL.md`, or paste it into the conversation.

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
- **`docs/tooling.md`** — widen coverage with existing safe scanners (read-only, stdout only) and pull
  dependency CVEs from a live advisory source (OSV), not model memory. Never install or auto-fix.
- **`docs/findings-quality.md`** — confidence scoring, false-positive challenge, stable IDs, a SARIF/JSON
  machine export, and a CI / non-interactive mode.

## Principles

- **Authorized only.** A target found in a repo does not authorize testing it.
- **Evidence over status codes.** `HTTP 200` is not proof; every mutation needs a separate read
  and a verified rollback.
- **No harm.** No DoS, brute force, enumeration, RCE, or damage to real data.
- **Tools for breadth, humans for logic.** Lean on scanners and live CVE data for coverage and
  freshness; keep manual reasoning for authorization and business logic.

## vs. scanners (when to use this)

Dedicated scanners win on breadth, speed, determinism, and fresh data; this plugin folds those
strengths in (safe existing scanners + live OSV data + SARIF export + CI mode) while adding what
they miss: **authorized, evidence-based testing of horizontal/vertical/tenant authorization and
business-logic workflows** with real A/B accounts and matched control/test pairs.

- **SAST** (Semgrep, SonarQube): great for code patterns; blind to runtime authorization/tenancy.
- **DAST** (StackHawk, NightVision, 42Crunch): great for crawl/fuzz; weak on business logic and
  per-object ownership. These skills test it deliberately, without enumeration or DoS.
- **SCA** (Sonatype, Endor, JFrog): deep dependency graphs; `audit-dependencies` queries live OSV
  data and existing audit tools read-only, then confirms manually.

Use a scanner for continuous, automated breadth; use these skills for a careful, authorized,
reproducible audit that reasons about authorization and workflows.

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
  tooling.md
  findings-quality.md
scripts/
  link-skills.sh            # link skills into ~/.agents/skills and ~/.claude/skills
skills/
  security/
    audit-backend/
      SKILL.md
      agents/openai.yaml    # Codex / OpenAI interface descriptor
    audit-access-control/{SKILL.md, agents/openai.yaml}
    audit-api/{SKILL.md, agents/openai.yaml}
    audit-uploads/{SKILL.md, agents/openai.yaml}
    audit-dependencies/{SKILL.md, agents/openai.yaml}
```

## Roadmap

- **Next:** `microservice-interdependency` skill — map inter-service dependencies and produce a
  security report, plus machine-readable export (e.g. SARIF) alongside the Markdown report.
- Repo tooling (versioning, skill validation) once the skill set grows.

## License

MIT — see [LICENSE](./LICENSE).
