# Manuscript

Keep current chapter drafts and revisions here. Use consistently ordered filenames. Git records revision history, and the [archive](../07-archive/) holds retired drafts that still need to be easy to find.

## Drafting workflow

1. Open the [manuscript index](INDEX.md). It tracks reading order, working titles, draft status, approximate word count, and outline references. The story target is **6,000–9,000 words**.
2. Create a `drafts/` directory here when you start writing. Copy the [chapter template](templates/chapter.md) for a whole chapter or the [scene template](templates/scene.md) for each major scene. Use stable, zero-padded filenames such as `drafts/01.md` or `drafts/01-02.md`.
3. Enter the file path in the index and write below the optional YAML metadata. Fill in the metadata only when useful. Use the timeline field for when events happen in the story world. Use the index for the order in which readers encounter them.
4. Keep working titles, statuses, and approximate word counts current in the index. Count manuscript text and exclude metadata and headings. For a chapter split into scenes, give each scene its own row and count.

The index supports one file per chapter or several scene files under one chapter number. Use `01` for a whole chapter or `01.01`, `01.02`, and so on for its scene rows. List rows in reading order and use only one of these layouts per chapter. Keep the file path as inline code, relative to this folder. Use `—` for a file you have yet to create.

Use the [continuity checker](../scripts/CONTINUITY.md) to compare explicit draft annotations with locked Story Bible facts.

## Assemble a single Markdown manuscript

From the repository root, run:

```sh
python3 04-manuscript/assemble.py > /tmp/weight-of-the-thread.md
```

The script reads file paths from the index in row order, removes leading YAML metadata, adds numbered chapter headings, and inserts Markdown scene breaks between successive scene files. A template with an empty body produces no text. Each listed file with manuscript text is included regardless of draft status. An export with no manuscript text exits with a message. Use a fresh output path for each export you want to keep.
