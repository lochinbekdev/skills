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
base URL, in-scope vs out-of-scope hosts/modules, audit window and rate limit, **outbound
network consent** (e.g. querying `api.osv.dev` or other advisory sources — see `tooling.md`),
two lowest-role accounts **A** and **B** plus any control-role accounts and, for cross-tenant
work, a lowest-role account in a *different* tenant (see `test-accounts.md`), identifiable
test objects for A and B, any non-account prerequisites (inert file fixtures, a running
processor/toolchain), and which create/update/delete/transition/field actions are authorized
and reversible. Do not ask again for anything already provided in the conversation.

## Phase 3 — Explain the plan
Once the user answers, restate concisely: which workflows/endpoints will be tested, the
A/B and control-role handoffs, which mutations will run and how they roll back, what is
**blocked** for missing data, and that the single report is the only file written
(`write-boundary.md`). Keep it short; no action yet.

## Phase 4 — Wait for "go"
Start real HTTP tests and mutations only after an explicit go ("boshla" / "start" / "go").
Until then, continue only read-only analysis. If the user changes scope mid-run, re-confirm
before testing the changed part.

## Depth: quick, standard, deep

An audit has a budget — tokens, time, request rate. Agree the depth in Phase 2 (default
**standard**) and state it in the report's scope section, so a shallow run never reads as a
thorough one:

| Depth | What runs | Use when |
|---|---|---|
| `quick` | Static only. Recon, then the highest-risk blocks: authentication, authorization, injection, secrets. No live requests. | A first look, a small budget, or no environment. |
| `standard` | Every applicable skill, static plus live tests on the highest-risk workflows, with the agreed accounts. | The default. |
| `deep` | Every applicable skill, every workflow and branch end to end, all role handoffs, tooling breadth. | A release gate or a formal audit. |

Whatever the depth, **order the work by risk** — authentication and authorization first, then
injection and uploads, then dependencies and configuration — and **protect the report**: if a
limit (tokens, time, quota, rate) is approaching, stop testing and write the report with what
is established. An audit that runs out of budget with no report has delivered nothing. Every
block not reached is `not-tested — budget`, and the title carries `PARTIAL AUDIT`.

## Scope: full or diff

Default scope is the whole in-scope system. When the user asks to audit **a change** — a pull
request, a branch, a commit range — use **diff scope** instead:

1. Establish the range (`git diff --name-status <base>...<head>`, read-only) and state it.
2. Audit the changed code **and what it reaches**: a changed controller pulls in its routes,
   middleware, policies and the models it writes; a changed dependency pulls in its advisories.
   A diff read without its call sites misses the authorization check that was never added.
3. Report only findings **introduced or exposed by the change**. A pre-existing problem the
   change merely touches is listed separately as `pre-existing`, not attributed to it.
4. Coverage blocks untouched by the change are `not-tested — outside diff scope`.

Diff scope is `quick` or `standard` depth; it has no live-test obligation unless the user
supplies an environment running the changed code.

## When to skip the interview
A skill that needs no live access or test data — it only reads the repo already in scope —
runs directly without phases 2–4 (e.g. `audit-dependencies`). It still respects the
write boundary and reports blocked items where confirmation is genuinely required.

## Static-only engagement (no live env / no accounts / no human)
A very common case: you have the repo but there is no reachable environment, no test
accounts, or no human to answer Phase 2. Do **not** stall. Instead:
1. Still do Phase 1 recon, and **write the Phase 2 Q-round into the report as a deliverable**
   (the questions a human would need to answer to enable runtime testing).
2. Perform the skill's checks **statically** as far as the code allows — trace
   input → guard → ownership/tenant/permission → sink → response/state, read config and
   middleware, and record concrete code-level findings with confidence `likely`/`unconfirmed`.
3. Mark every runtime/authenticated test `blocked` with the reason (no env/accounts).
4. The audit is still `PARTIAL AUDIT` for runtime, but state explicitly that **static
   coverage is complete** (every in-scope file/route reviewed) so a legitimate code-only
   review does not read as half-abandoned. See `report-standard.md` "Adapting the structure".
