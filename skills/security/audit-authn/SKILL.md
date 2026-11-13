---
name: audit-authn
description: Audit authentication and session handling — login, credential storage, password reset, MFA, JWT and session lifecycle, SSO/OAuth and service-issued user tokens. Use for login, session, token, password-reset, MFA or SSO security review.
---

# Authentication and session audit

Focused skill for how a system decides **who** a caller is — before authorization decides what
they may do. Read first: `references/intake.md`, `references/test-accounts.md`,
`references/write-boundary.md`, `references/report-standard.md`, `references/tooling.md`,
`references/findings-quality.md`.

Owns coverage blocks **A** (authentication), **B** (session and token lifecycle) and **C**
(federated identity) of `references/report-standard.md`. Finding IDs use the prefix `AUTHN-`.

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
Follow `references/intake.md`: map the authentication surface yourself read-only — guards,
middleware, token issuers, login/reset/MFA/SSO endpoints, session store — then ask the user,
in one round of numbered `Q1/Q2…` questions with recommended answers, only the gaps (test
environment, accounts A and B, whether a login attempt or a password reset on a test account
is authorized, any second factor or SSO test identity). Explain the plan, then send real
requests **only after an explicit "boshla"/"go".** Static review may proceed before that.

## Map first
For every way a caller can become authenticated, record: the endpoint or flow, the credential
it accepts, what it issues (cookie, JWT, opaque token, API key), where that is validated, its
lifetime, and how it is revoked. Machine and service identities count: a client credential
that can mint a user token is an authentication path.

## Checks (record a result for every item)
- **Credential handling** — password hashing algorithm and cost, comparison in constant time,
  no credential or token in logs, URLs, error messages or responses; default and fallback
  credentials in code or config.
- **Login** — user enumeration through response, status, timing or reset flow; lockout and
  throttling present and not bypassable by header or parameter; CAPTCHA enforced server-side.
  **Verify by reading the code and one or two agreed attempts — never by brute force.**
- **Password reset and change** — token entropy, single use, expiry, binding to the account;
  host-header and redirect poisoning of the reset link; whether a reset or change revokes
  existing sessions; whether the current password is required to change it.
- **MFA** — enforced at the server on every path, including API, mobile, SSO and
  "remember this device"; the second step cannot be skipped by calling the post-MFA endpoint
  directly; recovery codes and enrolment changes need re-authentication.
- **Tokens (JWT and opaque)** — algorithm pinned (no `none`, no HS/RS confusion), signature
  and `exp`/`nbf`/`aud`/`iss` actually verified, secret strength and rotation, sensitive data
  in claims, and **server-side revocation**: does logout, password change, role change or
  deactivation invalidate a token already issued?
- **Sessions** — identifier regenerated at login and privilege change (fixation), idle and
  absolute timeout, cookie flags (`Secure`, `HttpOnly`, `SameSite`), concurrent-session
  policy, logout that destroys the session server-side.
- **Role or context selection** — where a user picks a role, tenant or organization after
  login, the selection is checked against what that user actually holds, and a token for one
  context cannot be replayed in another.
- **Federated identity (SSO, OAuth/OIDC, SAML)** — `state` and nonce, redirect URI exactly
  matched, code and token exchange bound to the client, ID token signature and audience
  verified, account linking that cannot be hijacked by an unverified email or identifier.
- **Service-issued user tokens** — any endpoint where a machine client obtains a token *for a
  user* (impersonation, token exchange, "login as"). Which identifier does it trust, is that
  identifier bound to a verified identity, are privileged users excluded, is it audited?
- **Identity derived from the network** — roles or trust granted by source IP, header or
  proxy position; check the trusted-proxy configuration that makes that claim spoofable.

## Rules
- **No brute force, no credential stuffing, no account lockout**, and no password reset on any
  account other than the agreed test accounts. One or two agreed attempts prove a control;
  volume proves nothing more and harms the system.
- Token forgery and tampering are tested **only against your own test account's token**, and
  only as an authorized test. Never forge a token to set up another test
  (`references/test-accounts.md`).
- A finding that an authentication control is *missing* needs the code path that shows it; a
  finding that it is *bypassable* needs a matched pair — the control working, then the bypass.
- Authorization questions — whose object, which role — belong to `audit-access-control`. Hand
  them over rather than widening this skill.

Fold all results and evidence into the single report (`references/report-standard.md`), written
in **English by default** (or the user's chosen language). When delegated by the orchestrator,
write no file and return findings as that standard's "Returning findings as a delegated
companion" describes.
