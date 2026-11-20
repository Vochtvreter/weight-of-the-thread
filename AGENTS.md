# Collaboration guidelines for The Weight of the Thread

## Canon authority

The [Story Bible](01-story-bible/README.md) is the authoritative source of established story facts. Before proposing or editing anything that depends on story facts, read the relevant files in the current checkout, including the Story Bible and any affected character profiles, outlines, or manuscript chapters. Read the [project README](README.md) and the README for the section you are editing.

Earlier conversations, drafts, outlines, research, and archived material can provide context or reveal contradictions. Verify claims against the current Story Bible even when a prior conversation described them as settled. Apply these statuses when reading or writing story material:

| Status | Meaning |
| --- | --- |
| **LOCKED CANON** | An established fact approved by the author and recorded in the Story Bible. Treat it as binding for continuity and seek approval before changing it. |
| **PROVISIONAL IDEAS** | Brainstorming, proposals, alternate versions, and other possibilities awaiting a decision. Label them as provisional whenever you cite or develop them. |
| **OPEN QUESTIONS** | Unresolved decisions or contradictions that need the author's input. Track them in [Open Questions](OPEN_QUESTIONS.md) with links to the relevant files. |

Keep speculative ideas out of statements of established fact. A brainstorm, a working draft, or a repeated suggestion never grants canon status. If a material fact has no clear status, flag the uncertainty and ask the author when a decision is needed to proceed.

## Propose, review, and apply changes

1. **Check for contradictions before editing.** Compare the requested change with the relevant locked entries and affected drafts. Identify conflicting statements and cite their file paths and sections or entry IDs. If sources disagree or an edit would depend on an unresolved decision, surface the conflict before editing the affected material. Continue independent work where possible.
2. **Propose the specific change.** Before changing, removing, demoting, or adding locked canon, describe the current canon, the proposed wording or decision, the reason for it, and its effects on characters, chronology, technology, and affected files as applicable. Link to the relevant sources. Mark the proposal provisional while review is pending.
3. **Obtain explicit approval.** The author must approve the specific canon change before it is applied. General editing permission, brainstorming, and silence do not count as approval. If the approved scope is ambiguous or the proposal changes materially during review, ask the author to confirm the revised decision.
4. **Apply the approved scope and verify continuity.** Update the Story Bible and any explicitly approved downstream files. Recheck the affected entries and drafts against the approved decision. Report discrepancies or dependent edits that remain outside the approved scope.
5. **Record the decision.** Add a dated entry to [CHANGELOG.md](CHANGELOG.md) summarizing the approved change, with links to the affected Story Bible entries and a brief account of what changed. If it resolves an open question, record the decision in [Open Questions](OPEN_QUESTIONS.md) and link to where it was applied.

## Machine-readable canon status

For new or explicitly updated standalone canon entries, proposals, and question files, use YAML front matter at the top of the Markdown file when one status applies to its story material. Use a stable, repository-unique `canon_id` for each entry and keep it when a file moves or its status changes. Use one of the exact `canon_status` values `locked`, `provisional`, or `open_question`.

```yaml
---
canon_id: example-entry
canon_status: provisional
---
```

For files with entries of different statuses, use a labeled heading for each entry and omit the file-level `canon_status`. Move an entry into a standalone file if it needs machine-readable metadata. A missing, unknown, or conflicting status requires review. Metadata records a decision, and only the author's approval can authorize promotion to `locked`.

## Manuscript and preservation

- When editing the manuscript, check character knowledge, motivations, relationships, and established arcs. Check scene order and elapsed time, and honor established technology capabilities and limits. Flag any continuity issue before changing the affected passage.
- Preserve earlier drafts through Git history. Before replacing an important draft that exists only as uncommitted work, preserve that version. Keep retired drafts and important rejected ideas accessible in [the archive](07-archive/README.md), with context and a link to any successor.
- Never delete artwork, chapters, or research without explicit permission. Preserve existing paths and filenames unless the requested change calls for moving or renaming them.
- Use Markdown for text and keep edits within the requested scope. Add story content or revise the manuscript only when the author asks. Record significant project changes in the changelog and obtain the author's approval before committing or pushing.
