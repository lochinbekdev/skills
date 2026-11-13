# lochinbekdev / skills

Small, composable **security** skills for AI agents, installable as a plugin in Claude Code
and Codex — like npm/composer/pip, but for agent skills.

Each skill has a **narrow scope**, its own operating rules, and shares three cross-cutting
standards so every audit behaves the same way.

## Install

Pick one route per agent — installing two gives you every skill twice. The wording here is
copied from [`.agents/install-block.md`](./.agents/install-block.md); change it there first.

<details>
<summary><strong>Claude Code</strong></summary>

```bash
/plugin marketplace add lochinbekdev/skills
/plugin install lochinbekdev-security@lochinbekdev
```

Updates itself by default. The five focused skills are model-invoked, so "audit the uploads in
this project" reaches them. The orchestrator is user-invoked — name it:

```bash
/lochinbekdev-security:audit-backend
```

Installed outside the plugin (the symlink route below), the same skill is `/audit-backend`.

</details>

<details>
<summary><strong>OpenAI Codex</strong></summary>

```bash
codex plugin marketplace add lochinbekdev/skills
codex plugin add lochinbekdev-security@lochinbekdev
```

Updates itself at startup. **Restart Codex afterwards**, or the skills stay undiscovered.
Codex has no per-skill slash command. Plugin-bundled skills are namespaced by the plugin, so
invoke with `$lochinbekdev-security:audit-backend`, or run `/skills` to browse. For live HTTP testing use an interactive session or `-s workspace-write`;
under `codex exec -s read-only` every request fails with `Operation not permitted` and the
audit reports zero executed workflows.

This pair has not been run end to end yet — it needs the manifest on the default branch
upstream. Until then, use the symlink route below.

</details>

<details>
<summary><strong>Any other agent, or a local checkout</strong> (manual updates)</summary>

```bash
git clone https://github.com/lochinbekdev/skills
cd skills
./scripts/link-skills.sh
```

Symlinks every skill into `~/.agents/skills` (Codex and other generic agents) and
`~/.claude/skills` (Claude Code outside the plugin), pruning links it made earlier that now
dangle. `git pull` updates them in place; restart the agent to pick up new skills. You can also
point an `AGENTS.md` at a skill's `SKILL.md`, or paste it into the conversation.

</details>

## Skills

| Skill | Invocation | Scope |
|---|---|---|
| `audit-backend` | user only | Orchestrator — runs a full, stack-agnostic backend audit and writes the single report. |
| `audit-access-control` | model or user | Horizontal / vertical / cross-tenant authorization and field-permission tests with A/B accounts. |
| `audit-api` | model or user | Routes, injection, SSRF, CORS, headers, and business-logic abuse. |
| `audit-uploads` | model or user | Upload → storage → processing → serving, archive extraction (zip-slip), download authz. |
| `audit-dependencies` | model or user | Dependencies, lockfiles, runtime versions, CI/CD, and secret exposure (read-only). |
| `audit-microservices` | model or user | Inter-service dependency map and trust-boundary audit: s2s authn/authz, identity/tenant propagation, network exposure, SSRF pivots, queues, shared DBs. |

An audit sends live requests against a real system, so the orchestrator never starts on the
model's own initiative: a human names it. The focused skills stay reachable by name or by
description, because the orchestrator calls them.

## Shared standards (`docs/`)

> `docs/` is the canonical source. Because an installed skill is loaded by its own directory and
> cannot resolve a repo-root path at runtime, each skill bundles these as `references/<doc>.md`
> next to its `SKILL.md`. Edit under `docs/`, then run `scripts/sync-docs.sh` to refresh the copies.

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
- **`docs/harness-notes.md`** — repo-facing, not bundled: how Claude Code and Codex differ in
  practice (delegation, reference-file access, sandbox network, invocation) and what the skills
  do about it, recorded from real runs.
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

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) — `docs/` is the single source for the shared
standards, `python3 scripts/validate-repo.py` is what CI runs, and skill names carry no vendor
prefix. Vulnerabilities in the skills themselves: [SECURITY.md](./SECURITY.md). Release history:
[CHANGELOG.md](./CHANGELOG.md).

## Layout

```
.agents/
  install-block.md          # canonical install wording; README copies it
  plugins/marketplace.json  # Codex marketplace catalog entry
.github/
  workflows/validate.yml    # runs scripts/validate-repo.py on every push and PR
.claude-plugin/             # Claude Code manifests
  marketplace.json
  plugin.json
.codex-plugin/              # Codex plugin manifest (publisher, category, prompts)
  plugin.json
docs/
  intake.md
  report-standard.md
  test-accounts.md
  write-boundary.md
  tooling.md
  findings-quality.md
  harness-notes.md          # what differs between agents, from real runs
scripts/
  validate-repo.py          # names, descriptors, manifests, reference sync
  link-skills.sh            # link skills into ~/.agents/skills and ~/.claude/skills
  sync-docs.sh              # copy the shared standards into each skill's references/
skills/
  security/
    audit-backend/
      SKILL.md
      agents/openai.yaml    # Codex / OpenAI interface descriptor
    audit-access-control/{SKILL.md, agents/openai.yaml}
    audit-api/{SKILL.md, agents/openai.yaml}
    audit-uploads/{SKILL.md, agents/openai.yaml}
    audit-dependencies/{SKILL.md, agents/openai.yaml}
    audit-microservices/{SKILL.md, agents/openai.yaml}
```

## Roadmap

- **Shipped:** `audit-microservices` — inter-service dependency map and trust-boundary audit,
  with the standard report and SARIF/JSON export.
- **Next:** run the Codex plugin install end to end once the manifest is on the default
  branch, then record it in [`.agents/install-block.md`](./.agents/install-block.md).
- **Next:** repo tooling (skill validation against the Codex and Claude schemas) and CI eval
  cases as the set grows.

## License

MIT — see [LICENSE](./LICENSE).
