# Evidence review worksheet

This is a proposed working format for the repository owner or an agent with
access to original messages, rollouts or upstream decision records. It is not
a completed attribution and does not require a rollout to exist for upstream
work. Use the companion [requirement register](REQUIREMENT_PROVENANCE.md) to
select a concrete statement. Split grouped rows before assigning different
origins, reasons or statuses to individual clauses.

For the separate fork-policy proposal, use the
[item-level source index](FORK_PROVENANCE_REVIEW.md). It supplements the
main-source register without adopting those policies or completing their origin review.

## One record per instruction or independently decidable clause

Copy this block for each reviewed ID. Empty fields mean **not yet checked**,
not absent evidence, disproved origin, rejection or approval.

```text
Requirement ID / exact statement:
Observed document + immutable commit + heading/line range:
Document lineage (copied from where, independently of requirement origin):
Previous provisional origin / rationale / applicable status:
Evidence review state: not examined | primary checked | secondary only | conflicting | source unavailable
Origin category and originating actor, where evidenced:
Origin evidence locator (message/turn ID or upstream issue/commit; speaker role):
Evidence context/range and optional source-file hash:
Short redacted quotation or precise paraphrase supporting this exact clause:
What the evidence does NOT establish / contrary evidence:
Original rationale explicitly documented, or unknown:
New reviewer rationale or inference (separate; assumptions and alternatives):
Applicable/adoption status and scope at the inspected revision:
Later confirmation: actor, exact message, confirmed scope, date; or none found in searched evidence:
Execution/release/task state (separate from rule approval):
Recommended disposition: retain | amend | replace | investigate (not origin):
Previous -> proposed classification; reason for correction; reviewer/date:
Successor/superseded rule ID, if any:
Remaining searches / unavailable sources / owner of next step:
```

## Evidence handling

A concrete user instruction can establish explicit user origin for its actual
scope. An assistant proposal followed later by specific user confirmation keeps
its agent origin and gains the separately evidenced confirmation status. A
reason inferred now is not a recovered historical rationale. A contributor name,
Git author, user-story format, "must", repeated text, silence or a general
request to continue establishes neither original requester nor item-level
confirmation. A source hash identifies bytes, not authority or correctness.

Check the surrounding exchange and chronology. Do not mistake a quoted request,
compacted summary, model-generated claim or tool result for a direct user message.
Do not search for or import hidden reasoning. A rollout may be only a lead; use
upstream commits, issues, design notes or a named/versioned interface where those
are the actual sources. "Imported from upstream" is document lineage, not proof
that each rule is a platform mandate. Verify claimed external requirements
against the concrete version and scope before classifying them that way.

Preserve the previous provisional assessment when correcting it; do not rewrite
the originating actor when adoption changes. Do not decide conflicts by majority
of repeated copies. Record both claims and the unresolved question. Keeping an
operative legacy rule while recording its unknown origin is valid. Changing or
retiring it needs its own supported decision; origin is not a quality ranking.

## Public-repository boundary

Only place publication-safe evidence references and minimal redacted extracts
here. Keep private rollouts and fuller context in an appropriately restricted
location; the public record may use an opaque locator with access limitations.
Do not publish raw histories, credentials, personal paths or private project
names to fill a cell. Permission to use a PR as a review worksheet is not
permission to publish the source conversation. Session-attribution manifests
remain identifier-only; this worksheet belongs outside that manifest.

## Origin and adoption of this worksheet

The user explicitly requested separation of requirement origin, rationale and
applicable status in conversation `6a9e453e-97a0-83eb-8590-0a0bc0d2be7c` and,
after checkpoint 005, expressly welcomed using PRs as review templates for a
person or agent holding original rollouts. The category vocabulary and initial
retrospective approach were described by the user as another agent's proposal.
This field layout, clause IDs, evidence states and handling procedure are the
current reviewer's design proposal, not individually confirmed implementation
details. The user's general continuation does not approve existing rules.
