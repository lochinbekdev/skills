---
name: audit-retest
description: Verify fixes against an earlier security audit report — replay each finding's reproduction and report fixed, still-open or regressed. Use after remediation, for a retest, re-audit or fix verification.
---

# Retest: verify fixes against an earlier report

Takes an existing report produced by these skills and answers one question per finding: **is
it fixed?** It does not hunt for new problems; that is a fresh audit. Read first:
`references/intake.md`, `references/test-accounts.md`, `references/write-boundary.md`,
`references/report-standard.md`, `references/findings-quality.md`.

## Non-negotiable invariants

Some harnesses cannot read a file outside the working directory, so a sandbox may block the
`references/` files above. They are the full rules; these five hold even when you cannot open
them, and you state in the report which references you could not read:

1. **Authorized scope only.** A host, domain, IP or credential found in the repo does not
   authorize testing it. Live requests and mutations need an explicit "boshla"/"go".
2. **Read-only.** The audit writes exactly one file, the report (delegated companions write
   none; where nothing can be written, the report is the final message). No fixes, installs,
   migrations, seeds or auto-fixers; no REPL or database client without explicit
   authorization; a `GET` whose handler writes is a mutation. Record `git status` before and
   after.
3. **Evidence or nothing.** `HTTP 200` is not proof. Every claim carries a `path:line` or a
   matched control/test request pair; every mutation gets a separate read and a verified
   rollback; every finding carries `confirmed` / `likely` / `unconfirmed`. Credentials and
   tokens never appear in the report or the chat.
4. **Inventory is not the deliverable.** Summarise with counts, cap any inventory table at 30
   rows, and never paste file trees, directory listings or raw tool output as a section.
5. **Incomplete means `PARTIAL AUDIT`.** If a required test did not run, say so in the title
   and the summary with the blocker, and never claim the system is secure.

## How this skill starts
1. **Locate the report.** Default `SECURITY_AUDIT_REPORT.md` at the project root; otherwise ask
   for its path. Read its baseline commit, scope, accounts and finding list. If it has no
   stable finding IDs or no reproduction steps, say so: those findings can only be re-reviewed
   statically, and are reported as such.
2. **Establish what changed.** `git log <baseline>..HEAD` and `git diff --stat <baseline>..HEAD`,
   read-only. A finding whose code is untouched is almost certainly still open — check it
   anyway, it is cheap.
3. **Reconfirm scope** per `references/intake.md`. The earlier authorization does not carry
   over: ask, in one round of `Q1/Q2…` questions with recommended answers, whether the same
   environment, accounts and reversible mutations are still authorized, and wait for an
   explicit "boshla"/"go" before any live request. With no environment, retest statically.

## Per finding
Work through every finding in the report, in severity order, keeping its **original ID**:

1. **Replay the original reproduction exactly** — same actor, same request, same matched
   control — against the current build. Do not improve the test first; an altered test cannot
   say whether the original problem is gone.
2. **Then challenge the fix.** A fix that blocks the reported request but not its neighbours
   is not a fix: try the same flaw through the other verb, the sibling endpoint, the other
   role, the batch or export variant, the alternate encoding. Read the patch to see whether
   it removed the cause or only the symptom.
3. **Check the fix did not break the legitimate path.** Rerun the control request: the owner
   must still be able to do what the policy allows.
4. **Assign one status:**
   - `fixed` — the original reproduction fails, the variants fail, the control still works.
     Needs the same evidence standard as a confirmed finding; reading the patch alone gives
     `fixed (static)`, stated as such.
   - `partially-fixed` — the reported request is blocked but a variant succeeds. Record the
     variant as evidence; the finding stays open under its ID.
   - `still-open` — the original reproduction still succeeds.
   - `regressed` — it was recorded fixed in an earlier retest and reproduces again.
   - `not-retested` — blocked, with the reason (no environment, account gone, feature removed).
   - `accepted-risk` — only when the user states the risk was accepted; record who and when.

## New problems seen on the way
A retest is not a licence to ignore something serious. If the fix introduced a new flaw, or
one is plainly visible in the changed code, record it under a **new** ID with the skill
prefix `RT-`, clearly separated from the retest table, and recommend a focused audit of that
area. Do not go looking beyond the changed code.

## Deliverable
Update the **same report** rather than writing a second file: add a dated **Retest** section
with the new baseline commit, a table of every finding (ID, severity, previous status, new
status, evidence ID), the per-finding evidence, and an updated progress ledger. Leave the
original findings text intact so the history reads straight through. If the original report
cannot be modified, write `SECURITY_RETEST_REPORT.md` at an agreed path and say so. Counts go
in the summary: fixed, partially-fixed, still-open, regressed, not-retested.

Keep `PARTIAL AUDIT` in the title while any finding is `not-retested`. Never state that the
system is secure: a retest says which reported problems are closed, nothing more.
