# Security report standard (shared)

Every audit in this plugin produces **one Markdown report**. The orchestrator and every
focus skill conform to this structure, so reports read the same regardless of which skill
ran. This is the shared security report standard for the plugin.

## Output location
- Default filename: `SECURITY_AUDIT_REPORT.md`.
- Default location: the audited project root, unless the user or project agrees on another
  path (e.g. a dedicated `security/` or `work/` directory). Confirm the path once, then keep
  it stable across sessions. Do not invent nested directories the user did not agree to.
- **Read-only target:** if writing into the project is not allowed (a read-only checkout,
  a repo you must not touch, a CI dir), write the report to an agreed path **outside** the
  target and state where. Writing the report must never be the thing that violates the
  write boundary.
- This report is the **only** file the auditor writes (see `write-boundary.md`).
- **Nowhere to write:** in a sandbox that permits no writes at all, deliver the complete
  report as the final message instead, and say in its first line that no file was written
  and why. Do not shorten it and do not skip sections because it is going to chat.

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

## Inventory is not the deliverable

The inventory exists to prove coverage, not to fill the report. It is summarised, never dumped:

- **Aggregate, then cap.** Give counts first (routes, controllers, services, models, jobs,
  migrations, dependencies). Any inventory table stays at **30 rows or fewer**; past that,
  group the rest and give the group totals. A full per-item listing goes in an appendix, and
  only when the user asked for one.
- **Never paste a file tree, a directory listing, or raw tool output** as a section. Evidence
  is a `path:line` reference or a sanitized request/response pair, not a listing.
- **Counts are not coverage.** State inventory counts and executed-test counts separately, and
  never let the first imply the second.
- **A report with no findings and no executed tests is not a report.** If nothing could be
  tested and nothing was traced, say that in one short paragraph with the reason and the
  blocker, mark it `PARTIAL AUDIT`, and stop. Do not substitute an inventory for results.

## Coverage blocks A–Q

"Coverage" in every skill means these seventeen blocks. Each gets one status —
`tested` / `reviewed` / `not-applicable` / `not-tested` — with a reason, and each has an
owning skill, so a gap is visible rather than assumed:

| Block | Area | Owner |
|---|---|---|
| A | Authentication: login, credential handling, password reset, MFA | `audit-authn` |
| B | Session and token lifecycle: issue, expiry, revocation, binding | `audit-authn` |
| C | Federated identity: SSO, OAuth/OIDC, service-issued user tokens | `audit-authn` |
| D | Horizontal authorization: object ownership | `audit-access-control` |
| E | Vertical authorization: role and privilege separation | `audit-access-control` |
| F | Tenant isolation: region, organization, district | `audit-access-control` |
| G | Field-level authorization and mass assignment | `audit-access-control` |
| H | Input handling and injection: SQL, NoSQL, command, template | `audit-api` |
| I | SSRF and outbound requests | `audit-api` |
| J | Browser-facing controls: CORS, CSRF, headers, cookies, XSS | `audit-api` |
| K | Business logic: workflow state, limits, races | `audit-api` |
| L | Upload, storage and file processing | `audit-uploads` |
| M | File serving and download authorization | `audit-uploads` |
| N | Dependencies and runtime versions | `audit-dependencies` |
| O | CI/CD, build supply chain, secrets and configuration | `audit-dependencies` |
| P | Service-to-service trust boundaries, queues, shared datastores | `audit-microservices` |
| Q | Error handling, logging, debug surfaces, rate limiting | `audit-backend` |

A focused skill run on its own reports only its own blocks and marks the rest `not-tested —
outside this skill`. Block P is `not-applicable` for a single-service system.

## Returning findings as a delegated companion

When the orchestrator delegates to a focused skill, that skill is not the report's author:

- **Write no file.** Only the orchestrator writes the report. Return findings in the reply.
- **Use the skill's own ID prefix**, so parallel companions cannot collide:
  `AUTHN-` (`audit-authn`), `AC-` (`audit-access-control`), `API-` (`audit-api`),
  `UP-` (`audit-uploads`), `DEP-` (`audit-dependencies`), `MS-` (`audit-microservices`).
  The orchestrator's own findings use `SA-`; new problems seen during a retest use `RT-`. A skill run standalone uses the same prefix.
- **Return, per finding:** ID, title, severity, confidence, CWE, the coverage block, evidence
  (`path:line` or a sanitized request/response pair), the false-positive challenge, and the
  retest criterion. Then the status of each coverage block it owns, and its blockers.
- **Return no inventory.** Counts only; the orchestrator already holds the inventory.

The orchestrator merges, deduplicates by root cause, and keeps the companions' IDs unchanged
so a finding can be tracked across re-audits and retests.

## Adapting the structure per skill
The sections above are written for a full runtime authorization/workflow audit. A focused or
static-only run keeps the same skeleton but **marks inapplicable sections `not-applicable`
with a one-line reason** rather than padding them, and **adds the artifact its skill produces**:
- `audit-dependencies`: a dependency/CVE table and lockfile status; sections 4 (workflow
  matrix) and the A/B handoff parts of 2 are usually `not-applicable`.
- `audit-microservices`: a service-dependency map and a per-edge trust-boundary matrix in
  section 3, and cross-service chains in section 6.
- `audit-uploads` / `audit-api`: the endpoint/pipeline inventory in section 3.
- `audit-authn`: the authentication-path map (flow, credential, what it issues, lifetime,
  revocation) in section 3.
- `audit-retest`: a dated **Retest** section appended to the existing report, with the
  per-finding status table; the original findings text stays intact.
- A **static-only** run (no env/accounts, per `intake.md`) keeps section 2's unanswered items
  as the Q-round, marks runtime rows `blocked`, and states that static coverage is complete.
Never delete a section silently; `not-applicable` with a reason preserves the coverage contract.

## Evidence status labels
Label every result explicitly: `confirmed`, `partial`, `blocked`, `not-applicable`,
`not-tested` — each with a reason. Signature/scanner/file-count output does not establish a
complete manual audit or real API testing. Each finding also carries a **confidence**
(`confirmed`/`likely`/`unconfirmed`) and a **stable ID** per `findings-quality.md`.

## Machine-readable export (optional, agreed)
Alongside this Markdown report, emit a machine-readable findings file (SARIF 2.1.0 preferred,
JSON fallback) when the user asks or when running in CI, per `findings-quality.md`. The
Markdown stays the human source of truth; the export is written only to an agreed path under
the write boundary. Dependency CVEs come from a live advisory source, not model memory
(`tooling.md`).
