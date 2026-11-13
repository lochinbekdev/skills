---
name: lochinbekdev-audit-access-control
description: Test horizontal, vertical, and cross-tenant authorization on a backend using two lowest-role test accounts (A/B) and control roles, with matched control/test request pairs. Use when the user wants broken-access-control / IDOR / privilege-escalation / tenant-isolation testing, or runs /lochinbekdev-audit-access-control.
---

# Authorization testing (A/B + control roles)

Focused skill for **broken access control**: horizontal (A↔B at the same level), vertical
(low role → high-role operation), cross-tenant isolation, and protected-field tampering.
Read first: `references/intake.md`, `references/test-accounts.md`, `references/write-boundary.md`, `references/report-standard.md`, `references/findings-quality.md` (confidence scoring, false-positive challenge, stable IDs).

## How this skill starts
Follow `references/intake.md`: first inspect the code read-only and map the resources, owners,
and tenant boundaries yourself; then ask the user — as one round of numbered `Q1/Q2…`
questions with recommended answers — only the gaps (A/B lowest-role accounts, control
roles, identifiable test objects, authorized reversible mutations). Explain the test plan,
then run real requests and mutations **only after an explicit "boshla"/"go".** Read-only
code tracing may proceed before that.

## Prerequisite
Two separate accounts **A** and **B**, both at the system's **lowest authenticated role**,
plus a separate control account per higher role the workflow needs. Reach each by **normal
login**; verify real role/permission/tenant via the project's identity endpoint (discover it; it is often not `/me`). If missing, mark dependent tests
**blocked** and continue read-only code tracing (input → guard → ownership/tenant/permission
check → sink → response/state).

## Test sequence (per in-scope resource/flow)
1. **Identity** — A and B via the project's identity endpoint (often not `/me` — e.g. `/api/account/profile`; discover the real one): confirm both are lowest-role and sessions are separate.
2. **Legitimate control** — A → A's object; B → B's object. Establish the operation works and
   the business policy is understood.
3. **Horizontal** — A's session → B's object; B's session → A's object. Did cross-account
   access become available contrary to policy?
4. **Lists & files** — read/list/detail/download/export with ID, filter, nested, batch, and
   scope variants. Was another account's content/metadata/file returned?
5. **State changes** — authorized update/delete on own vs other object; confirm persistence
   with a **separate read**.
6. **Vertical** — lowest role → an operation reserved for a higher role; use a control account
   to prove the legitimate path. Was a privileged business operation actually performed?
7. **Field authorization** — submit role/permission, owner, and tenant fields via body/query/
   nested fields. In a **separate** request verify effective permissions actually changed and a
   previously denied operation became available — a server echo of the field is **not** proof.
8. **Rollback** — reverse every mutation; verify restoration with a separate read/identity check.

## Rules
- Matched pairs: change only one factor (session / object id / tenant / field); keep everything
  else equal; link both evidence IDs and name the changed factor.
- Report **horizontal**, **vertical**, and **cross-tenant** failures **separately**. An A/B test
  within one tenant is **not** a cross-tenant test — without distinct tenant contexts, mark
  cross-tenant **blocked**.
- `HTTP 200` ≠ exploitation (check body, empty results, login HTML, different object, reflection).
  `403` ≠ unchanged state (needs a separate read). `404` may be valid concealment only when a
  matched control proves the object/route exists and policy supports it.
- Every mutation: original → small change → separate read → rollback → rollback read. If rollback
  fails, stop mutating that area and record the residual change, risk, and required operator action.

Fold all results and evidence into the single report (`references/report-standard.md`), written in **English by default** (or the user's chosen language).
