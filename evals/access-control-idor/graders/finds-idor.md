---
type: llm
weight: 2
---

The response reports that `InvoiceController::show` (GET /invoices/{id}) returns an invoice
without checking that it belongs to the requesting user — a horizontal authorization / IDOR
flaw. It must NOT report the same flaw for `index` (which filters by user_id) or for
`destroy` (which calls the policy).
