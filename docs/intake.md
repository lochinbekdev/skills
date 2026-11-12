# Intake protocol (grill → plan → go)

Skills that need live access or test data follow this four-phase protocol before any
real test. It mirrors a short interview: find facts yourself, ask only what is missing,
explain the plan, and start only on the user's explicit go. Read-only static review of
code already in context may proceed during phases 1–3; **runtime tests and any mutation
wait for phase 4.**

## Phase 1 — Self-recon (never ask what you can find)
Do a small, read-only inspection of the project first. Finding facts is the skill's job,
not the user's. Detect and record (for the report and the plan):
- Stack: language/runtime, framework, datastores, package manager, lockfiles.
- Surface: routes/controllers, auth model (cookie/JWT/OAuth/MFA), middleware/policies,
  tenant/module boundaries, jobs/CLIs, external integrations.
- Candidate business workflows and the endpoints behind them.
Only after this, identify the gaps that genuinely require the user.

## Phase 2 — Ask the gaps (grilling style)
Ask the missing items in **one round** of numbered questions, each with a **recommended
answer**, worded so "yes" accepts the recommendation:

```
❓ **Q1** - **<title>**: <question + options>
➡️ <recommended answer>
```

Ask only what Phase 1 could not establish. Typical gaps: authorized test environment /
base URL, in-scope vs out-of-scope hosts/modules, audit window and rate limit, two
lowest-role accounts **A** and **B** plus any control-role accounts (see
`docs/test-accounts.md`), identifiable test objects for A and B, and which
create/update/delete/transition/field actions are authorized and reversible. Do not ask
again for anything already provided in the conversation.

## Phase 3 — Explain the plan
Once the user answers, restate concisely: which workflows/endpoints will be tested, the
A/B and control-role handoffs, which mutations will run and how they roll back, what is
**blocked** for missing data, and that the single report is the only file written
(`docs/write-boundary.md`). Keep it short; no action yet.

## Phase 4 — Wait for "go"
Start real HTTP tests and mutations only after an explicit go ("boshla" / "start" / "go").
Until then, continue only read-only analysis. If the user changes scope mid-run, re-confirm
before testing the changed part.

## When to skip the interview
A skill that needs no live access or test data — it only reads the repo already in scope —
runs directly without phases 2–4 (e.g. `dependency-supply-chain`). It still respects the
write boundary and reports blocked items where confirmation is genuinely required.
