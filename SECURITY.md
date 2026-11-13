# Security policy

## Reporting a vulnerability in this repository

Open a private security advisory through GitHub's **Security → Report a vulnerability** on
this repository. Please do not open a public issue first.

What is in scope here is the repository itself: an instruction that could make an agent act
outside the boundaries these skills promise — writing to a project it was told to only read,
testing a host nobody authorized, exfiltrating evidence, or running a destructive command.
Those are the failures that matter in a skill, and they are treated as vulnerabilities.

## Findings your audit produced

Findings about *your* system belong to you. Do not post a report produced by these skills,
or any part of it, in an issue or pull request here: it carries hostnames, endpoints,
credentials and business data. If you want to show a behaviour problem, quote the shortest
decisive line with the identifying parts removed.

## What these skills do and do not do

Every skill is read-only by instruction: the only file it writes is its report. They ask for
authorization before touching a live system, and they refuse to treat a host, domain or
credential found in a repository as permission to test it. They do not apply fixes, install
packages, or run denial-of-service, brute-force or enumeration attacks.

None of that is a sandbox. The agent running these skills has whatever access you gave it,
and an instruction is not an enforcement boundary. Run audits against systems you are
authorized to test, in an environment whose blast radius you accept.
