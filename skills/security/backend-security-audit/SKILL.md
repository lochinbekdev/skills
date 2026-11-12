---
name: backend-security-audit
description: Run an authorized, evidence-based backend security audit of an existing project and produce one reproducible report. Use when the user asks to audit, pentest, or security-review a backend (any stack), or runs /backend-security-audit. Stack-agnostic; read-only; delegates to focused security skills.
---

# Backend security audit (orchestrator)

You are conducting an **authorized** security audit of one existing backend. Stack-agnostic
(PHP, Node.js, Python, Go, Java, Ruby, .NET, Rust, …). Goal: find weaknesses, test every
in-scope business workflow end-to-end through **real APIs** with A/B and control roles, and
write an evidence-based report a developer can reproduce. **Applying fixes is out of scope.**

Follow these shared rules exactly — read them before acting:
- `docs/intake.md` — the grill → plan → go protocol: recon first, ask the gaps, explain, wait for go.
- `docs/write-boundary.md` — the single-file, read-only write boundary and baseline check.
- `docs/test-accounts.md` — test accounts, normal login, matched control/test pairs.
- `docs/report-standard.md` — the one deliverable, its structure, and output location (**report in English by default**).

## How this skill starts
Do **not** jump straight into testing. Follow `docs/intake.md`:
1. **Self-recon (Phase 1).** Inspect the repo read-only and establish stack, routes, auth
   model, tenant boundaries, and candidate workflows yourself — do not ask what you can find.
2. **Ask the gaps (Phase 2).** Put the missing items to the user as one round of numbered
   `Q1/Q2…` questions, each with a recommended answer (test env/base URL, in/out-of-scope,
   audit window/rate, accounts A/B + control roles, test objects, authorized mutations).
3. **Explain the plan (Phase 3).** Restate what will be tested, the A/B/control handoffs,
   mutations and rollback, blocked items, and that only the report is written.
4. **Wait for go (Phase 4).** Start real HTTP tests and mutations only after an explicit
   "boshla"/"start"/"go". Read-only static analysis may continue before that.

## Deliverable
One report, `SECURITY_AUDIT_REPORT.md` (default location: the audited project root, or an agreed path), written in **English by default** (or the user's chosen language), in the structure
of `docs/report-standard.md`. If any required practical test is incomplete, the title and
summary must be marked **`PARTIAL AUDIT`**.

## Procedure
1. **Baseline.** Record project root, time/zone, commit, and `git status` (see write-boundary).
2. **Scope & authorization.** Use what the conversation already provides; ask only for missing
   items, grouped into one request, per `docs/test-accounts.md` §"Accounts to request". A domain,
   IP, or credential found in the repo does **not** authorize testing it.
3. **Technology profile & inventory.** Record exact runtime/framework versions, dependencies
   and lock references, datastores, auth model, tenant boundaries, proxy/WAF, containers/CI,
   and integrations. Inventory every route, controller/service/model, middleware/policy,
   job, CLI, config, and migration. Tabulate in the report. Mark unknowns.
4. **Business workflow inventory.** Identify **every** workflow (ordinary ones too). Assign
   stable IDs (`WF-001`), map each to endpoints and A–Q blocks. Missing access is a blocker,
   not a reason to drop a workflow.
5. **Delegate the focused work** to the companion skills, feeding each the shared rules:
   - `authz-testing` — horizontal/vertical/tenant authorization and field-permission tests.
   - `api-surface-audit` — routes, input handling, injection, SSRF, CORS, business logic.
   - `upload-storage-security` — upload → storage → processing → serving, archive extraction.
   - `dependency-supply-chain` — dependencies, lockfiles, runtime versions, CI/CD, secrets.
   Each returns findings and evidence to fold into the single report; do not duplicate captures.
6. **Real tests.** Static review alone is insufficient. Run operation-level authz tests and
   full end-to-end workflow runs with A/B and control roles, using matched control/test pairs
   (`docs/test-accounts.md`). `HTTP 200` is not proof; every mutation needs a separate read and
   a verified rollback.
7. **Coverage & A–Q.** For every inventory item and every A–Q block, mark reviewed / tested /
   not-applicable / not-tested with a reason. Do not claim coverage from sampling.
8. **Report.** Write the single report per the standard (English by default). Keep a progress ledger inside
   it so the audit can resume. End the chat with report path, status, main confirmed results,
   workflow counts, and blockers — no sensitive evidence in chat.

## Hard limits
No DoS, brute force, broad enumeration, account lockout, RCE, or harm to real data. No pivot to
third-party or production targets. Request separate authorization for any new target or impact.
