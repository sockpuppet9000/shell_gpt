# ShellGPT Fork / Patch Backlog

This queue governs the public fork relationship and the separate credential-heavy
PR #1. Upstream product work remains owned by `TheR1D/shell_gpt`. Real API keys,
OAuth tokens, account IDs, auth files, prompts, caches and provider responses must
never enter Git, public CI, issues or examples.

## SGF-001 — Name the fork owner and intended role

- Priority: P0 governance
- Status: Open

- [ ] Decide whether this repository is a temporary contribution fork, maintained
  private-use patch line, archival snapshot or future independently named fork.
- [ ] Name the human owner and review/expiry date.
- [ ] Keep canonical upstream explicit.
- [ ] Prevent the unchanged snapshot from being presented as an original product.

## SGF-002 — Maintain an exact upstream/fork manifest

- Priority: P0 provenance
- Status: Open

- [ ] Record stable upstream repository ID/URL and reviewed upstream commit.
- [ ] Record fork `main`, every fork-only branch and commit/tree identity.
- [ ] Classify upstream-ahead, fork-ahead and divergent state.
- [ ] Recompute before sync, PR review, release, archive or deletion.
- [ ] Record tags and signed/release provenance where relevant.

## SGF-003 — Decide disposition of auth PR #1

- Priority: P0 security/product
- Status: Open

Choose and document one path:

- [ ] sanitize, test and propose an upstream-compatible feature;
- [ ] keep as a clearly named private/personal patch;
- [ ] redesign against an officially supported credential contract;
- [ ] close as obsolete/unsupported;
- [ ] split generic and account-specific pieces.

Do not merge it into `main` merely to reduce branch drift.

## SGF-004 — Verify provider and account authorization

- Priority: P0 authority/compliance
- Status: Open

- [ ] Establish whether the proposed browser/token exchange is officially
  supported for the intended account and product.
- [ ] Confirm API/subscription/billing separation and permitted token audience.
- [ ] Review provider terms, client ID, scopes, issuer and redistribution.
- [ ] Define unsupported/account-policy-denied states.
- [ ] Avoid relying on an implementation observed from another application as
  standing integration authority.

## SGF-005 — Stop sharing another application's auth file implicitly

- Priority: P0 confidentiality/integrity
- Status: Open

- [ ] Decide whether ShellGPT may read Codex auth state at all.
- [ ] Do not rewrite `${CODEX_HOME}/auth.json` without an explicit versioned
  ownership/interoperability contract.
- [ ] Separate application-owned credentials where possible.
- [ ] Add no-write inspection and explicit migration/import flow.
- [ ] Define concurrent access, backup, rollback and corruption recovery.

## SGF-006 — Version credential storage schema and permissions

- Priority: P0 credential security
- Status: Open

- [ ] Define schema/version, allowed fields and migration.
- [ ] Create parent directories/files with restrictive permissions independent of
  `umask`.
- [ ] Reject symlinks, unsafe ownership and special files.
- [ ] Write through same-filesystem temp + flush/`fsync` + atomic replace.
- [ ] Preserve last known good state and record partial/cleanup failures.

## SGF-007 — Bind account, issuer, client and token audience

- Priority: P0 authorization
- Status: Open

- [ ] Record expected provider issuer, client ID, account and organization.
- [ ] Validate discovery/metadata where applicable rather than trusting hidden CLI
  overrides.
- [ ] Reject arbitrary issuer/client destinations by default.
- [ ] Verify token audience, scopes, expiry and account binding before reuse.
- [ ] Prevent wrong-account credential reuse.

## SGF-008 — Harden OAuth callback flow

- Priority: P0 security
- Status: Open

- [ ] Bind loopback host/port and exact redirect URI.
- [ ] Keep PKCE/state/session generation and comparison well tested.
- [ ] Add callback request limits, Host checks and one-shot expiry.
- [ ] Stop/clean server and browser flow on success, failure, timeout and signal.
- [ ] Test occupied ports, malicious callbacks, replay and race conditions.

## SGF-009 — Redact authentication errors and diagnostics

- Priority: P0 confidentiality
- Status: Open

- [ ] Never include token endpoint response bodies, authorization URLs, codes,
  tokens or account IDs in ordinary errors/logs.
- [ ] Use structured error categories and bounded private diagnostics.
- [ ] Add seeded-secret tests across exceptions, stdout/stderr and CI.
- [ ] Review HTTP library debug/proxy/trace behavior.

## SGF-010 — Remove silent import-time credential effects

- Priority: P0 authority/predictability
- Status: Open

- [ ] Do not read shared auth files or exchange tokens merely by importing the CLI
  module.
- [ ] Make credential discovery explicit and observable.
- [ ] Avoid silently mutating `os.environ`.
- [ ] Distinguish inspect, login, refresh, import and use capabilities.
- [ ] Add opt-in policy and tests for disabled/absent/malformed state.

## SGF-011 — Define logout, revoke, rotate and uninstall

- Priority: P0 credential lifecycle
- Status: Open

- [ ] Add exact application-specific logout/credential removal.
- [ ] Avoid deleting credentials still owned by Codex or another consumer.
- [ ] Define provider revocation and local rotation.
- [ ] Inventory caches, processes and backups after removal.
- [ ] Add incident response for token/API-key exposure.

## SGF-012 — Rebase and test against current upstream

- Priority: P1 correctness
- Status: Blocked on PR disposition

- [ ] Review all 13+ intervening upstream commits and current dependency/API
  contracts.
- [ ] Rebase/cherry-pick in a temporary branch with explicit conflict resolution.
- [ ] Run upstream unit/lint/type/integration checks using fake credentials.
- [ ] Add focused auth/storage/callback/precedence/concurrency tests.
- [ ] Do not use a real account as the first compatibility test.

## SGF-013 — Review shell/function execution safety

- Priority: P0 security
- Status: Open

- [ ] Map interactive, noninteractive, default-execute and function-call paths.
- [ ] Add command preview/confirmation and high-risk classification tests.
- [ ] Bound process runtime/output/children/environment/cwd/network.
- [ ] Review custom function provenance and local code execution.
- [ ] Prevent secrets read from local commands/files being returned to providers
  without explicit scope.

## SGF-014 — Define prompt/cache/config privacy

- Priority: P0 privacy
- Status: Open

- [ ] Inventory config, chat/request caches, roles, functions and shell integration.
- [ ] Set private permissions, retention, expiry and cleanup.
- [ ] Sanitize error/diagnostic output and public bug reports.
- [ ] Add private/operator/share-safe schemas and synthetic fixtures.

## SGF-015 — Preserve upstream license and attribution

- Priority: P0 rights
- Status: Open

- [ ] Preserve MIT notice and upstream authorship.
- [ ] Record authorship/copyright for fork-only files.
- [ ] Keep upstream product screenshots/docs under their original context.
- [ ] Review third-party dependency notices before distribution.
- [ ] Do not imply upstream endorsement of the auth patch.

## SGF-016 — Prevent accidental fork releases

- Priority: P0 operations
- Status: Open

- [ ] Disable or protect PyPI/container/release workflows in the fork.
- [ ] Remove personal release credentials and environments.
- [ ] Require explicit fork name/version/package coordinates for any independent
  release.
- [ ] Verify resulting artifact provenance and source.
- [ ] Clarify that `pip install shell-gpt` installs upstream.

## SGF-017 — Define sync, archive and delete lifecycle

- Priority: P1 governance
- Status: Open

- [ ] Decide fast-forward/rebase/reset policy for `main`.
- [ ] Preserve or close fork-only PRs before destructive ref changes.
- [ ] Inventory dependents, clones, CI, links and credentials.
- [ ] Archive when only historical contribution value remains, or delete after a
  separately approved dependency review.
- [ ] Record that deletion does not recall clones/packages.

## SGF-018 — Publication and branding policy

- Priority: P0 permanent while noncanonical
- Status: Permanent

- [ ] Do not create independent logo, social preview, portfolio claim or product
  screenshot for the unchanged upstream snapshot.
- [ ] Use synthetic credential/auth examples for any patch documentation.
- [ ] Link canonical upstream prominently in fork-specific status material.
- [ ] Publish general improvements upstream where accepted.

## Decisions recorded

- Fork `main` is an exact upstream commit and was 13 commits behind at review.
- Open PR #1 is the only identified fork-specific feature line and is not on
  `main`.
- Upstream package/product authority remains with `TheR1D/shell_gpt`.
- Credential interoperability requires explicit official/product authorization.
- Public visibility is not release readiness.
