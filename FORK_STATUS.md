# ShellGPT Fork Status

Reviewed: **2026-07-25**

This public repository is a non-canonical personal fork/snapshot of
[`TheR1D/shell_gpt`](https://github.com/TheR1D/shell_gpt). The upstream README,
package identity, documentation links, license and product claims remain upstream
material.

> [!IMPORTANT]
> Install commands such as `pip install shell-gpt`, upstream container images and
> links under `TheR1D/shell_gpt` do not install or describe an independently
> released `sockpuppet9000` product.

> [!CAUTION]
> ShellGPT can send prompts, stdin, files, logs and conversation history to a
> configured model provider. It can generate and execute shell commands, invoke
> locally installed functions, modify shell integration files and retain API
> credentials, prompts, chats, roles and caches. Fork status does not reduce
> those upstream product risks.

## Verified topology

| Item | Reviewed state |
|---|---|
| Canonical upstream | `TheR1D/shell_gpt` |
| Fork default branch | `sockpuppet9000/shell_gpt:main` |
| Fork `main` head | `9615dfbec856c1e1822adc4d9e4a3a3035a002b0` |
| Relationship of that head | Exact commit present in upstream history |
| Reviewed upstream head | `a082bd5327ce0c4ef5a0284d9060e833be9444a6` |
| Upstream commits after fork `main` | 13 |
| Fork-only commits on `main` | None identified at reviewed head |
| Open fork feature work | PR #1 on `codex/integrate-sgpt-with-codex-login` |
| Independent package/release | None |
| Software license | Upstream MIT, Copyright 2023 Farkhod Sadykov |
| Recommended repository role | Personal patch/fork workspace, not canonical product source |

The exact comparison is time-bound. Recheck upstream and every local branch before
syncing, rebasing, releasing or archiving.

## Existing fork-only PR

Open PR #1 is titled:

```text
feat(auth): fallback to Codex auth.json for OPENAI_API_KEY
```

At the reviewed state it contains three commits and adds a large authentication
surface, including:

- automatic inspection of `OPENAI_API_KEY`, ShellGPT config and Codex
  `${CODEX_HOME}/auth.json`;
- browser-based OAuth/PKCE flow with a localhost callback server;
- token exchange and refresh helpers;
- storage of API key, ID/access/refresh tokens and account ID in the shared Codex
  auth file;
- import-time fallback that can place a discovered key into process environment;
- user-selectable hidden issuer and client-ID options;
- new tests and documentation.

That PR is not part of `main`, not an upstream feature and not an approved release
contract. It should remain isolated until its product, security, provider-policy,
credential-ownership and upstream-contribution questions are resolved.

## Authentication patch security boundary

The proposed patch needs explicit review of at least:

- whether the intended token/API-key exchange is an officially supported and
  permitted integration for this product and account class;
- whether ShellGPT should ever write or rewrite another application's auth file;
- owner, format, schema version, permissions, atomicity, backup and recovery for
  `${CODEX_HOME}/auth.json`;
- separation between ChatGPT subscription credentials and OpenAI API credentials;
- token audience, issuer, scopes, expiry, refresh, revocation and account binding;
- callback host/port, browser and state/PKCE behavior;
- arbitrary/overridden issuer and client-ID destinations;
- redaction of HTTP response bodies, authorization URLs, tokens and errors;
- silent import-time credential reads and mutation of `os.environ`;
- concurrent Codex/ShellGPT access and stale-write handling;
- logout, uninstall and incident response.

A local file containing a key or token is not proof that another application may
reuse it. A successful network exchange is not proof of support, billing model,
long-term compatibility or redistribution rights.

## Upstream product authority

The following remain owned by upstream unless a deliberate fork release says
otherwise:

- package name `shell_gpt` and CLI `sgpt`;
- PyPI installation and release version;
- container images;
- product README, screenshots and documentation;
- supported Python/provider/platform matrix;
- issues, security fixes and release history.

General bug fixes should normally be proposed upstream after sanitization and
tests. Organization- or account-specific behavior needs a clearly named private
patch line or an independently named fork.

## Shell and function execution boundary

The upstream product can:

```text
prompt/model response
  → generated shell command
  → operator prompt or configured default
  → local command execution
```

It can also load custom/default Python functions whose `execute` methods run when
the model selects them. The upstream README explicitly demonstrates arbitrary
shell execution and warns about destructive commands.

Before using or distributing a modified build, review:

- default execution behavior and noninteractive paths;
- command parsing, quoting and shell selection;
- function discovery, code provenance and permissions;
- environment, cwd, filesystem, network and child-process access;
- output/secret leakage back to model providers;
- timeouts, process-tree cancellation and resource limits;
- audit and confirmation boundaries.

## Credentials, prompts and caches

Potential private local state includes:

- `~/.config/shell_gpt/.sgptrc` and API credentials;
- chat and request caches;
- custom roles and functions;
- shell integration changes;
- prompt/stdin/file/log contents;
- provider base URLs and model/account metadata;
- Codex auth state if PR #1 is ever used.

Do not commit, paste or publish these artifacts. A public repository and MIT
license do not make user prompts, credentials, caches or provider responses
public.

## Sync and release policy

Until an explicit fork decision is made:

- do not publish PyPI packages or containers from this fork;
- do not reuse the upstream package/version as if fork binaries were upstream;
- do not enable deployment/release workflows with personal credentials;
- compare `main`, every fork-only branch and current upstream before sync;
- preserve the upstream MIT notice and authorship;
- keep fork-specific changes attributable and testable;
- document whether each patch is upstream-bound, private, obsolete or blocked.

A fast-forward of `main` must not silently erase or falsely imply inclusion of PR
#1. Conversely, merging PR #1 before reviewing upstream's intervening changes can
create a stale or unsupported credential implementation.

## Publication boundary

This repository is already public, but it is not an independent publication.
Public-facing work should be limited to:

- accurate fork status;
- upstream contribution links;
- clearly separated fork-only patch review;
- preserved license and attribution;
- synthetic credential/auth fixtures.

Do not create independent branding, social previews, screenshots, package releases
or portfolio claims for the unchanged upstream snapshot.

Detailed fork, auth and lifecycle work is tracked in
[`FORK_BACKLOG.md`](FORK_BACKLOG.md).
