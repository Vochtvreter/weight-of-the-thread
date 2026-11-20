# Continuity checker

From the repository root, run:

```sh
python3 scripts/check_continuity.py
```

To save the same Markdown report, redirect it to a separate file:

```sh
python3 scripts/check_continuity.py > /tmp/weight-of-the-thread-continuity.md
```

The checker uses the Python 3.10+ standard library. It reads Markdown files in [the Story Bible](../01-story-bible/) and throughout `04-manuscript/drafts/`, including drafts awaiting an index entry. It writes its report to standard output. The command exits with status 1 for invalid input, locked canon mismatches, or inconsistencies to review. Coverage gaps alone exit with status 0. Check the coverage section even when the command succeeds.

## Annotating facts

Put one optional `continuity_json: |` field in a file's opening YAML front matter and indent its JSON by at least two spaces. All three JSON keys are optional. Omit the field in files without checkable claims. The normal [manuscript assembler](../04-manuscript/README.md#assemble-a-single-markdown-manuscript) drops front matter in the compiled draft.

This example uses invented identifiers and values solely to show the format.

```yaml
---
continuity_json: |
  {
    "facts": {
      "character.example.name": "Example Name",
      "character.example.birth_year": 2070,
      "event.example-opening.year": 2100,
      "event.example-arrival.year": 2101,
      "habitat.example.population.at-arrival.people": 1200,
      "resource.example.amount.at-arrival.kg": 25,
      "location.example.name": "Example Deck",
      "term.example.name": "Example valve"
    },
    "ages": [{"character": "example", "year": 2101, "age": 30}],
    "before": [["event.example-opening.year", "event.example-arrival.year"]]
  }
---
```

- **Facts.** Use stable dotted keys. Match the property, entity, time or event, and units on both sides of a comparison. Population and inventory change, so include the relevant snapshot in the key. Write quantities as numbers. Names, locations, and terms are case-sensitive and compare exactly. Use a key for the official name only when the draft is asserting that name. An intentional alias or a character's mistaken statement can be left out of the annotations.
- **Ages.** Use the same character ID as in `character.<id>.birth_year`. With only a birth year and observation year, either age is possible depending on whether the birthday has passed. An incompatible age is reported. An agreed locked birth year takes precedence when assessing a draft age. Otherwise the checker uses the draft's own birth-year claim or an agreed reference.
- **Chronology.** Enter event years as positive integers and list facts as first-event and second-event pairs in `before`. The checker reports a later year preceding an earlier year. Same-year pairs, missing dates, and conflicting dates are reported as coverage gaps. Draft dates take precedence when checking an order against the draft, including an order declared in locked canon.
- **Authority.** A Story Bible file contributes baseline facts only when its front matter contains `canon_status: locked` under the [author approval workflow](../AGENTS.md#propose-review-and-apply-changes). Keep working proposals and open questions in their existing statuses. The checker also reports conflicting locked declarations and conflicting draft declarations using the same key. It does not choose a winner.

## What still needs a reader

The checker compares explicit annotations. It does not extract claims from prose or interpret free-form POV, timeline, and location metadata. An annotation can be stale, so verify it against the passage it describes. The checker does not infer terminology variants, convert units, reason about quantities across scenes, infer event order from chapter order, or resolve events within one year. It cannot assess narrative intent, unreliable narration, character knowledge, plausibility, or implied contradictions. A report with no findings only covers the annotated claims available to the checker.
