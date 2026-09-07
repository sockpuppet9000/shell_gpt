# Provisional requirement provenance and evidence-review map

## Scope and evidence boundary

Fork baseline `9615dfbec856c1e1822adc4d9e4a3a3035a002b0` (2025-07-17), tree
`16b003f800bff3fd5272756f65fdef4db7f9cb27`, is also an independently read
commit/tree in `TheR1D/shell_gpt`. Upstream document lineage is therefore known;
the originating requester or designer of each instruction is not established.
Inherited upstream text is neither this fork user's instruction nor automatically
a platform mandate. No change is proposed to upstream itself.

Read: complete README text, CONTRIBUTING, sgpt/role.py and scripts/test.sh;
root tree and selected recursive entries. The full application, every helper,
CI/tests, external wikis, providers and both parallel draft rule sets are not
fully reviewed. No local user role/configuration/credential store was inspected.
The long recursive tool response was display-truncated; no full-code audit claimed.

The four built-in prompt strings are covered line by line, including illustrative
clauses. A code template is not evidence that all installed role files contain
that template: create_defaults preserves existing files. The static source was
parsed without importing sgpt or running its default-role initialization.

All old rows remain **provisional at original-source level**, with documented
applicability separated from unknown origin. Rationale means a stated purpose
or explicit unknown, not a historical motive guessed now. No individual user
confirmation is asserted. Existing safeguards and contribution gates are not
cancelled by unknown provenance. Template creation is not model-behavior validation.

## Seeded review rows

| ID | Exact location / clause | Original origin | Rationale | Applicable status | Evidence question |
|---|---|---|---|---|---|
| SG-C01 | [CONTRIBUTING.md][source-1] — Find an Issue, first bullet: Find an issue, self-assign and signal interest. | Unresolved | Overall stated aim: smooth contribution; detailed original process rationale unknown. | Inherited contributor guidance. | Find upstream governance discussion; split selection, assignment and notification clauses. |
| SG-C02 | [CONTRIBUTING.md][source-1] — Find an Issue, second bullet: New ideas use a discussion, then support from at least a couple of people before an issue. | Unresolved | Unknown original reason for this approval threshold. | Inherited community intake process, not this user confirming a requirement. | Who chose the threshold and for which repository? Fork issues/discussions are disabled; no upstream issue is opened by this review. |
| SG-C03 | [CONTRIBUTING.md][source-1] — Find an Issue, third bullet: Urgent critical issues may go directly to a PR. | Unresolved | Urgency is stated; original exception policy source unknown. | Documented exception. | Find its original scope; do not use urgency to infer approval of unrelated work. |
| SG-C04 | [CONTRIBUTING.md][source-1] — Development / environment / dependencies: Strict types and listed lint/test/environment setup. | Unresolved | Tooling purpose visible; original tool selection unknown. | Existing development guidance; commands not executed here. | Trace typing/tool choices and distinguish examples from requirements imposed by a real interface. |
| SG-C05 | [CONTRIBUTING.md][source-1] — Start Coding: Follow existing style, modularity and frequent commits. | Unresolved | Stated goal: maintainability, review and progress documentation. | Inherited working guidance, not individually user-confirmed. | Which part is a specific requirement versus general contributor advice? |
| SG-C06 | [CONTRIBUTING.md][source-1] — Testing: Feature changes include tests; unverified code is not merged; test through sgpt arguments/output. | Unresolved | Stated goal: verify expected behavior. | Existing testing/merge gate, not a provenance confirmation. | Trace the introduction and test scope; a passing test does not prove requester identity. |
| SG-C07 | [CONTRIBUTING.md][source-1] — Pull Request: Run lint and referenced test script; describe changes and testing. | Unresolved | Stated goal: checks pass and reviewers can test. | Existing process; path typo corrected separately below. | Find the original command contract; distinguish a filename correction from a new testing policy. |
| SG-C08 | [CONTRIBUTING.md][source-1] — Code Review: Address reviewer feedback and collaborate. | Unresolved | Stated goal: refine code and quality. | Existing process. | Reviewer acceptance of code is not user confirmation of each requirement. |
| SG-P01 | [sgpt/role.py][source-2] — SHELL_ROLE, baseline line 16: Provide only {shell} commands for {os} without any description. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P02 | [sgpt/role.py][source-2] — SHELL_ROLE, baseline line 17: If there is a lack of details, provide most logical solution. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P03 | [sgpt/role.py][source-2] — SHELL_ROLE, baseline line 18: Ensure the output is a valid shell command. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P04 | [sgpt/role.py][source-2] — SHELL_ROLE, baseline line 19: If multiple steps required try to combine them together using &&. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P05 | [sgpt/role.py][source-2] — SHELL_ROLE, baseline line 20: Provide only plain text without Markdown formatting. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P06 | [sgpt/role.py][source-2] — SHELL_ROLE, baseline line 21: Do not provide markdown formatting such as ```. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P07 | [sgpt/role.py][source-2] — DESCRIBE_SHELL_ROLE, baseline line 24: Provide a terse, single sentence description of the given shell command. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P08 | [sgpt/role.py][source-2] — DESCRIBE_SHELL_ROLE, baseline line 25: Describe each argument and option of the command. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P09 | [sgpt/role.py][source-2] — DESCRIBE_SHELL_ROLE, baseline line 26: Provide short responses in about 80 words. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P10 | [sgpt/role.py][source-2] — DESCRIBE_SHELL_ROLE, baseline line 27: APPLY MARKDOWN formatting when possible. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P11 | [sgpt/role.py][source-2] — CODE_ROLE, baseline line 30: Provide only code as output without any description. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P12 | [sgpt/role.py][source-2] — CODE_ROLE, baseline line 31: Provide only code in plain text format without Markdown formatting. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P13 | [sgpt/role.py][source-2] — CODE_ROLE, baseline line 32: Do not include symbols such as ``` or ```python. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P14 | [sgpt/role.py][source-2] — CODE_ROLE, baseline line 33: If there is a lack of details, provide most logical solution. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P15 | [sgpt/role.py][source-2] — CODE_ROLE, baseline line 34: You are not allowed to ask for more details. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P16 | [sgpt/role.py][source-2] — CODE_ROLE, baseline line 35: For example if the prompt is "Hello world Python", you should return "print('Hello world')". | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P17 | [sgpt/role.py][source-2] — DEFAULT_ROLE, baseline line 37: You are programming and system administration assistant. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P18 | [sgpt/role.py][source-2] — DEFAULT_ROLE, baseline line 38: You are managing {os} operating system with {shell} shell. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P19 | [sgpt/role.py][source-2] — DEFAULT_ROLE, baseline line 39: Provide short responses in about 100 words, unless you are specifically asked for more details. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P20 | [sgpt/role.py][source-2] — DEFAULT_ROLE, baseline line 40: If you need to store any data, assume it will be stored in the conversation. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-P21 | [sgpt/role.py][source-2] — DEFAULT_ROLE, baseline line 41: APPLY MARKDOWN formatting when possible. | Unresolved | Unknown original rationale. | Built-in template; installed state not inspected. | Trace original request/design for this exact clause. |
| SG-L01 | [sgpt/role.py][source-2] — ROLE_TEMPLATE / create_defaults / _save: Role framing, create only absent defaults, and explicit overwrite interaction. | Unresolved | Historical rationale unknown; behavior visible in source. | Existing template/storage behavior; a role-file overwrite prompt is not blanket requirement approval. | Trace framing/storage choices. Existing installations may retain older or customized prompts. |
| SG-D01 | [README.md][source-3] — Installation / Docker / Docker + Ollama: Backend setup, credential/configuration examples and container usage. | Unresolved | Stated usage purpose; original local defaults and external contract sources not independently checked. | Inherited documentation; examples are not authority to install, send data or use credentials now. | Separate example values from actual local defaults and versioned provider requirements; no provider selected here. |
| SG-D02 | [README.md][source-3] — Shell commands / Shell integration: Generate then interact with a command, no-interaction option and hotkey integration. | Unresolved | Stated convenience of shell assistance. | Documented modes and examples, not user approval of generated actions or all rules. | Trace command-selection/interaction defaults and hotkey choice individually. |
| SG-D03 | [README.md][source-3] — Generating code / Chat / REPL: Code-only, named chats, temporary REPL and continuation examples. | Unresolved | Stated purposes: format-specific output and conversation continuity. | Documented behavior and illustrations. | Keep a continuation example separate from acceptance of all added requirements; compare documented and actual role choices. |
| SG-D04 | [README.md][source-3] — Function calling: Function schemas and examples of model-selected calls and retries. | Unresolved | Feature use is described; original authority-design rationale unknown. | Documentation with destructive-command warning, not current execution permission. | Which limits are local design choices? Do not treat example calls or model confidence as user authorization. |
| SG-D05 | [README.md][source-3] — Roles: Create/edit roles and APPLY MARKDOWN behavior. | Unresolved | Stated purpose: customization and presentation. | Documented local convention. | Trace the marker convention; editing a role does not prove origins of its inherited sentences. |
| SG-D06 | [README.md][source-3] — Request cache / Runtime configuration / argument list: Caching, paths, timeouts, model/color/function defaults and flags. | Unresolved | Caching purpose stated; exact thresholds/default reasons unresolved. | Documented parameter values; no current provider or installation guarantee. | Split individual values when assigning origins; a default in text is not a direct user request. |

[source-1]: https://github.com/sockpuppet9000/shell_gpt/blob/9615dfbec856c1e1822adc4d9e4a3a3035a002b0/CONTRIBUTING.md
[source-2]: https://github.com/sockpuppet9000/shell_gpt/blob/9615dfbec856c1e1822adc4d9e4a3a3035a002b0/sgpt/role.py
[source-3]: https://github.com/sockpuppet9000/shell_gpt/blob/9615dfbec856c1e1822adc4d9e4a3a3035a002b0/README.md

## Narrow correction and next pass

CONTRIBUTING's `scripts/tests.sh` points to no file in the inspected scripts tree;
the actual, read script is `scripts/test.sh`. The path correction is an **agent
inference from repository evidence**, proposed to make the existing instruction
resolvable. It is not a newly discovered user request, a removed test gate or a
claim that lint/tests were run. All other contributor text remains unchanged.

Use [the evidence worksheet](PROVENANCE_REVIEW_TEMPLATE.md) per atomic clause.
Record original message/turn or upstream decision, speaker, context, supporting
scope, rationale, separate adoption state and later specific confirmation.
Keep any previous provisional assessment and explain the correction. Most
upstream origins may require upstream discussion rather than personal rollouts.
No actual original rollout was available to this pass; do not invent one.

## Origin of this annotation workflow

The distinction itself is an explicit first user request in conversation
`6a9e453e-97a0-83eb-8590-0a0bc0d2be7c`. After checkpoint 005, the user expressly
welcomed PRs as templates for precise attribution by a person or agent holding
original rollouts. The five categories and retrospective approach were described
as another agent's proposal. These clause IDs, grouped documentation rows, the
worksheet and maintenance procedure are this reviewer's design proposal. The
filename correction is the separate evidence-based inference above. None of
these implementation details is treated as individually confirmed by "continue".

## Parallel drafts and remaining decisions

PR #1 at `6346458d88de119933a328fec9fa31e862f9f745` is an authentication draft;
PR #2 at `1de51b0d62ee2ad73dd3a462a066920a7049b9b2` adds fork-status/backlog
proposals. Metadata and #2's manifest were read, not both complete diffs or their
original task discussions. Their extra instructions, 18 fork packages, and source
claims need a separate evidence/coverage pass before combination. #2's existing
session entry is retained as self-declared contribution, not as rule approval.

README, all sgpt source including every prompt literal, scripts, tests, license,
packaging and workflows are unchanged. No package install, API/model request,
authentication, generated-command execution, shell integration, role generation,
upstream action or merge is performed. Lint/test commands and real behavior
evaluations remain unexecuted; this PR is a review draft, not feature approval.
