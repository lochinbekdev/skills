# Security report standard (shared)

Every audit in this plugin produces **one Markdown report**. The orchestrator and every
focus skill conform to this structure, so reports read the same regardless of which skill
ran. This is the shared security report standard for the plugin.

## Output location
- Default filename: `SECURITY_AUDIT_REPORT.md`.
- Default location: the audited project root, unless the user or project agrees on another
  path (e.g. a dedicated `security/` or `work/` directory). Confirm the path once, then keep
  it stable across sessions. Do not invent nested directories the user did not agree to.
- This report is the **only** file the auditor writes (see `docs/write-boundary.md`).

## Language
- **Default: English.** Write the report in English unless the user asks for another language.
- If the user requests a specific language, write the whole report in that language. Keep code,
  paths, HTTP, and identifiers verbatim regardless of language.

## Hard rules
- If any required practical test, workflow/branch, control-role case, browser check,
  reproduction, terminal effect, rollback verification, or coverage item is incomplete, mark
  the report **`PARTIAL AUDIT`** in both the title and the executive summary (use the natural
  equivalent phrase when writing in another language).
- Never claim the system is secure, or the audit complete, without evidence.
- Keep observed impact, reproduction reliability, and remediation status distinct.

## Mandatory sections (in order)
1. **Executive summary** — date, audit status, principal confirmed results, counts by
   severity and by evidence status, major coverage gaps, and workflow/transition execution
   counts (separate from endpoint and coverage-block counts).
2. **Scope & authorization** — environment/base URL, authorized hosts/modules, accounts,
   audit window, rate limits, prohibited actions, and the agreed test objects.
3. **Coverage inventory & results** — route/component/dependency map, full business workflow
   inventory, workflow↔endpoint mappings, what was reviewed and how, and
   not-applicable/untested areas. Inventory counts kept distinct from runtime coverage.
4. **End-to-end workflow coverage** — the workflow matrix: every workflow/branch, required
   step/state/role case, actual execution coverage, terminal-outcome evidence, rollback
   verification, and A/B/control-account handoffs linked to test/evidence IDs.
5. **Findings summary** — table of findings with severity/CWE, evidence status, and
   horizontal vs vertical vs cross-tenant classification.
6. **Detailed findings** — for each: a clear description, severity/CWE/CVE, matched-control +
   independent reproduction results, limitations, developer recommendation, and retest
   criteria. Deduplicate root causes; document attack chains and their gaps.
7. **Evidence records** — sanitized requests/actual responses, source excerpts, read/identity
   evidence, browser observations, advisory results. Every executed test links to evidence.
8. **Progress ledger & remediation roadmap** — last update time, env/build/commit, scope
   refs, stable workflow/test/finding IDs, completed/in-progress/pending/blocked work, next
   safe step, outstanding rollback rows, and advisory-only remediation priorities (no fixes
   applied).

## Evidence status labels
Label every result explicitly: `confirmed`, `partial`, `blocked`, `not-applicable`,
`not-tested` — each with a reason. Signature/scanner/file-count output does not establish a
complete manual audit or real API testing.
