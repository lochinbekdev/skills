# Changelog

Notable changes per release. Versions are the `version` field in
`.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`, which must agree.

## 0.4.0 — 2026-11-13

New skills:

- **`audit-authn`** — login, credential handling, password reset, MFA, JWT and session
  lifecycle, SSO/OAuth, and service-issued user tokens. The most serious findings in the
  baseline runs were authentication flaws that no skill owned.
- **`audit-retest`** — verifies fixes against an earlier report: replays each finding's
  original reproduction, challenges the fix with its variants, and reports `fixed`,
  `partially-fixed`, `still-open` or `regressed` under the original IDs.

New capabilities:

- **Depth** (`quick` / `standard` / `deep`) agreed at intake, with work ordered by risk and
  the report protected: when a limit approaches, testing stops and the report is written.
  A Codex run had spent its whole quota without producing one.
- **Diff scope** — audit a pull request, branch or commit range instead of the whole system.
- **Coverage blocks A–Q are now defined**, each with an owning skill. The orchestrator had
  been referring to them without any definition existing.
- **Delegation contract** — a delegated companion writes no file and returns findings under
  its own ID prefix (`AUTHN-`, `AC-`, `API-`, `UP-`, `DEP-`, `MS-`), so parallel companions
  cannot collide.
- A minimal **SARIF example** in the findings standard, and `scripts/validate-sarif.py`.
- **Evals** under `evals/`, run with `claude plugin eval`.

Tightened rules:

- REPLs and database clients (`tinker`, `rails console`, `psql`, …) need explicit
  authorization; a run had read role data straight from a database nobody had agreed to expose.
- A `GET` whose handler writes, dispatches or deletes is a mutation, out of scope under
  "GET only" and reportable as an unsafe method.
- Credentials are requested out of band, never repeated, never written to the report.
- With nowhere to write, the complete report is delivered as the final message.
- Fixed a garbled sentence in the orchestrator's inventory step.

## 0.3.1 — 2026-11-13

- Codex catalog keys (`policy.installation`, `policy.authentication`, `category`) move out of
  the Claude Code marketplace manifest, which ignores them, into a Codex marketplace manifest
  at `.agents/plugins/marketplace.json`.

## 0.3.0 — 2026-11-13

- **Breaking:** skill names are bare again — `audit-backend`, `audit-api`, and so on. Codex
  namespaces plugin-bundled skills itself, as `$lochinbekdev-security:audit-api`, so the
  0.2.0 names produced the vendor twice. Claude Code shows
  `/lochinbekdev-security:audit-api`; outside a plugin both harnesses use the bare name.
- `docs/harness-notes.md` records how that was established, so the wrong inference is not
  repeated.

## 0.2.0 — 2026-11-13

First release driven by running the skills headless against a real Laravel 12 backend with
both Claude Code and Codex.

- **Explicit delegation.** The orchestrator asks for one agent per companion skill, in
  parallel, and states the fallback for harnesses without sub-agents: run every applicable
  skill inline, in full. Codex had been doing the whole audit itself and finding a third of
  what Claude Code found on the same target.
- **Invariants restated in every `SKILL.md`.** A sandbox can block the bundled
  `references/` files — Claude Code, loading a skill through a symlink outside its working
  directory, could not open one. Authorized scope, read-only, evidence or nothing, inventory
  is not the deliverable, and `PARTIAL AUDIT` now survive that.
- **Report gates.** Aggregate counts first, 30 rows per inventory table, no file trees or raw
  tool output as a section, inventory counts separate from executed-test counts, and a report
  with no findings and no executed tests is a short blocker paragraph, not a dump.
- **Codex plugin manifest** (`.codex-plugin/plugin.json`) with publisher, category and starter
  prompts, so `codex plugin add` works like `/plugin install`.
- **Spec-compliant descriptors.** Every `agents/openai.yaml` `short_description` is within the
  documented 25-64 characters and carries a `default_prompt`.
- **The orchestrator is user-invoked** in both harnesses. An audit sends live requests and
  needs authorization, so the model does not start one on its own initiative.
- Descriptions trimmed to a trigger sentence plus a scope sentence, for Codex's skill-catalog
  budget.
- `scripts/link-skills.sh` prunes its own dangling links; `scripts/sync-docs.sh` bundles only
  the six shared standards.
- **Breaking (reverted in 0.3.0):** skills were renamed `lochinbekdev-audit-*`.

## 0.1.0 — 2026-11-12

- Six security skills: `audit-backend` (orchestrator), `audit-access-control`, `audit-api`,
  `audit-uploads`, `audit-dependencies`, `audit-microservices`.
- Six shared standards under `docs/`, bundled into each skill as `references/`.
- Claude Code plugin and marketplace manifests; `agents/openai.yaml` descriptors and a
  symlink script for Codex and other agents.
