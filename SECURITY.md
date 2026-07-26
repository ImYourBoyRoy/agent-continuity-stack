# Security Policy

## Supported versions

Security fixes target the latest published stable release and, while this
project remains pre-release, the newest release candidate. Older release
candidates may receive fixes only when a safe upgrade path requires them.

## Reporting a vulnerability

Use the canonical repository's
[private vulnerability-reporting form](https://github.com/ImYourBoyRoy/agent-continuity-stack/security/advisories/new).
Do not open a public issue with credentials, exploit details, private paths, or
sensitive logs.

Include:

- affected package and skill versions;
- affected clients and operating systems;
- the trust boundary that fails;
- minimal reproduction steps using disposable data;
- expected and observed behavior;
- impact, preconditions, and known mitigations.

Do not test against accounts, repositories, clients, or machines you do not own
or have permission to assess.

## High-priority security areas

- instruction replacement or precedence confusion;
- path traversal and malicious lifecycle records;
- symlink, junction, reparse-point, or special-file handling;
- backup consumption, corruption, or unsafe rollback;
- duplicate instruction or skill discovery;
- archive inventory or extraction bypass;
- credential, profile, or private-path disclosure;
- remote-code execution through unaudited helpers;
- false runtime-verification claims.

## Credential policy

The package does not require credentials. Maintainer tokens belong only in a
local ignored `.env` or an approved secret manager. Never commit a populated
environment file, paste a token into model instructions, package credentials in
an archive, or include them in diagnostic output.
