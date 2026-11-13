# Evals

Regression cases for the skills, run with `claude plugin eval`:

```bash
claude plugin eval . --runs 1            # every case, once
claude plugin eval . --case 'authn-*'    # one case
```

Each case hands the agent a small, deliberately flawed code sample **inside the prompt** and
grades the reply. The cases are static on purpose: an eval run starts in an empty directory
with no network and, on machines without a sandbox backend, no shell — so nothing here needs
a running application. They check the behaviour that is easy to lose in an edit:

| Case | What it guards |
|---|---|
| `access-control-idor` | The missing ownership check is found, and a code-only finding is not called `confirmed`. |
| `authn-token-mint` | A service endpoint that mints a user token from an unverified identifier is found. |
| `dependencies-no-invented-cves` | With no advisory source, version-specific CVE claims are `blocked`, not invented. |

All three also fail a reply that dumps an inventory or claims the system is secure. Live
behaviour — delegation, the "go" gate, rollback — still needs a real target; see
`docs/harness-notes.md`.

`evals/results/` is run output and is not committed.
