---
type: llm
weight: 2
---

The response reports, as its most serious finding, that `POST /client/sso/token` lets any
authenticated partner client obtain a full user token for ANY user by submitting that user's
national ID: the identifier is not bound to a verified identity, and privileged users
(e.g. administrators) are not excluded. A response that only discusses the login endpoint,
or that treats the SSO endpoint as fine, fails.
