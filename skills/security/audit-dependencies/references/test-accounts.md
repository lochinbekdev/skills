# Test accounts & authenticated testing (shared rule)

Referenced by `audit-access-control` and the orchestrator. Static code review is **not** a
substitute for real authenticated runtime tests.

## Accounts to request (one grouped request)
1. **Two separate accounts, A and B**, both holding the system's **lowest authenticated
   role**. Anonymous, admin, or an account merely named "user" does **not** satisfy this.
   If several minimal roles exist with no shared hierarchy, agree on one and document it.
   On a **two-dimensional model** (role level × tenant/region/org), "lowest role" means the
   least-privileged *level*; name both the level and the tenant for each account so it is
   unambiguous.
2. For **cross-tenant** testing, a **third lowest-role account in a *different* tenant**
   (region/org/district). A and B in the same tenant test horizontal access; they cannot
   test tenant isolation. Without a distinct-tenant account, mark cross-tenant `blocked`.
3. **Separate control accounts for every role the workflow needs** (reviewer, approver,
   operator, admin) — used only to prove legitimate handoffs and role separation.
4. Login method (cookie/JWT/OAuth/MFA), expected roles/permissions, memberships, and
   tenant/organization relationships.
5. Identifiable test objects owned by A and by B, plus the business authorization policy.
6. Which create/update/delete/transition/field/rollback actions are authorized per object,
   with agreed small test values, original states, and restoration method.

## Rules
- Reach every account through **normal login**. Never edit roles in the DB, fabricate or
  forge tokens, or bypass auth to set up a test.
- Keep each session **separately in memory**; never mix account tokens.
- Verify each account's real roles/permissions/tenant via the project's **identity endpoint**
  — this is often not `/me` (e.g. `/api/account/profile`, `/session`, `/whoami`); discover the
  real one from the routes. Do not assume an endpoint exists; if you cannot verify, say so and
  do not claim confirmation.
- A and B must **stay** at the lowest role. Do not promote them to prepare a test.
- If accounts, tenants, objects, connectivity, or authorization are missing, mark **only
  the dependent tests blocked** and continue independent read-only analysis.

## Matched control/test pairs (how every authz test runs)
Establish a successful legitimate request, then change **only one factor** (account/session,
object id, tenant context, or protected field), keeping method, endpoint shape, and
unrelated values equal. Link both evidence IDs and name the changed factor.
- `HTTP 200` alone is **not** proof of exploitation — check body for business errors,
  empty results, login HTML, a different object, or reflected input.
- A `403` does not prove state is unchanged — a state-changing test needs a **separate read**.
- Every mutation: original value → small change → separate read → rollback → rollback read.
- Keep mutations small, authorized, reversible. No brute force, enumeration, lockout, DoS,
  or harm to real data.
