---
name: audit-microservices
description: Map the inter-service dependencies of a microservice system and audit the security of every trust boundary between services — service-to-service authn/authz, identity and tenant propagation, network exposure, SSRF pivots, queues, and shared datastores. Produces a service dependency map plus the standard report. Use when the user wants a microservice / service-mesh / inter-service / distributed-system security review, or runs /audit-microservices.
---

# Microservice interdependency & trust-boundary audit

Monoliths hide their trust boundaries inside one process; microservices expose them on the
network. This skill maps which services call which, then audits the security of each edge —
the gaps scanners miss. Read first: `references/intake.md`, `references/write-boundary.md`,
`references/test-accounts.md`, `references/report-standard.md`, `references/tooling.md`,
`references/findings-quality.md`.

## How this skill starts
Follow `references/intake.md`:
1. **Self-recon (read-only).** Discover services and edges yourself before asking. Sources:
   `docker-compose*.yml`, Kubernetes/Helm manifests, service-mesh config (Istio/Linkerd/Envoy),
   API-gateway/ingress config, service registry/discovery, `.env`/config service URLs, HTTP
   clients and SDK calls in code, message-queue producers/consumers, and shared DB connections.
2. **Ask the gaps (`Q1/Q2…`).** Only what recon cannot establish: the full set of in-scope
   services and repos/paths (services may live in separate repos — request their locations),
   the authorized test environment per service, which edges are internal vs internet-facing,
   and accounts per service (`references/test-accounts.md`). Do not ask what you can read.
3. **Explain the plan.** Present the draft service map and which edges you will test.
4. **Wait for go.** Static mapping may proceed now; real cross-service requests wait for
   an explicit "boshla"/"go".

## 1. Build the service dependency graph
Inventory every service: name, language/runtime, exposed ports/routes, upstream callers,
downstream callees, transport (REST/gRPC/queue/event), and the datastores it owns or shares.
Record each **edge** as `caller -> callee` with transport and purpose. Mark whether each
service/edge is internal-only or reachable from the internet (via gateway/ingress). Tabulate
the graph in the report; a service or edge that cannot be confirmed is a coverage gap, not an
omission.

## 2. Audit each trust boundary (per edge)
For every `caller -> callee` edge, check:
- **Service authn.** How does the callee authenticate the caller — mTLS, signed service token,
  JWT, shared secret, network trust only, or nothing? Flag unauthenticated internal edges.
- **Service authz.** Does the callee enforce what the caller may do, or trust any caller that
  reached it? Flag "trust the network / trust the gateway" assumptions.
- **End-user identity & tenant propagation.** Is the end user's identity/tenant carried and
  **re-verified** at the callee, or does the callee act with ambient service privilege on the
  user's behalf? This is the classic **confused-deputy / broken object-level authz across
  services** — delegate the concrete A/B and cross-tenant runtime tests to `audit-access-control`.
- **Network exposure.** Is an "internal" service or admin endpoint actually reachable from the
  internet (missing ingress rule, default-exposed port, debug endpoint)? Confirm reachability;
  do not assume from naming.
- **Boundary input validation.** Does the callee re-validate input it receives from another
  service, or trust it because it is "internal"? Trace input -> guard -> sink at the boundary.
- **SSRF pivots.** Can a user-controlled URL/param at one service cause a server-side request
  into another internal service or metadata endpoint? Use only agreed in-scope targets.
- **Secrets for service-to-service.** How are s2s credentials stored, rotated, and scoped?
  Report class and location without exfiltrating values (`references/tooling.md`).
- **Async / queues / events.** Can a message be forged, replayed, or sent cross-tenant? Is the
  consumer's trust in the message justified, and is the producer authenticated?
- **Shared datastores.** Do multiple services share a DB/schema, bypassing another service's
  authorization by writing its tables directly? Flag ownership/boundary violations.

## 3. Cross-service attack chains
Combine edge findings into chains, e.g.: internet-facing service with weak input validation ->
SSRF -> unauthenticated internal service -> shared DB write that bypasses the owner's authz.
Document each chain with its edges, preconditions, evidence, and gaps (`references/findings-quality.md`).

## Rules
- Read-only write boundary (`references/write-boundary.md`): only the report plus an agreed SARIF/JSON
  export. No installs, no deploys, no `docker compose up`, no cluster mutation.
- Real cross-service tests reuse matched control/test pairs and accounts (`references/test-accounts.md`);
  `HTTP 200` is not proof, every mutation needs a separate read and rollback.
- Keep horizontal, vertical, and cross-tenant results distinct; an edge test within one tenant is
  not a cross-tenant test.
- No DoS, no broad enumeration, no pivot to third-party or production systems, no RCE.
- Give each finding a stable ID and confidence; challenge false positives (`references/findings-quality.md`).

Fold the service map, edge matrix, chains, and evidence into the single report
(`references/report-standard.md`), written in **English by default** (or the user's chosen language).
