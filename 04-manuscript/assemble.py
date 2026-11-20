"""Assemble the manuscript files listed in INDEX.md into Markdown."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
INDEX_HEADER = "| Order | Working title | Status | Approx. words | Outline reference | File |"


def index_rows():
    lines = (ROOT / "INDEX.md").read_text(encoding="utf-8").splitlines()
    if INDEX_HEADER not in lines:
        raise ValueError("Missing manuscript table in INDEX.md.")
    previous_order = (0, 0)
    for line in lines[lines.index(INDEX_HEADER) + 2:]:
        if not line.startswith("|"):
            break
        fields = re.split(r"(?<!\\)\|", line.strip().strip("|"))
        if len(fields) != 6:
            raise ValueError(f"Expected six columns in index row: {line}")
        order, *_, file_entry = (field.strip() for field in fields)
        if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", order):
            raise ValueError(f"Invalid manuscript order: {order}")
        chapter, _, scene = order.partition(".")
        chapter_number, scene_number = int(chapter), int(scene or 0)
        if chapter_number < 1 or (scene and scene_number < 1):
            raise ValueError(f"Manuscript numbering starts at 1: {order}")
        if (chapter_number, scene_number) <= previous_order:
            raise ValueError(f"Manuscript rows must be in increasing order: {order}")
        if chapter_number == previous_order[0] and previous_order[1] == 0:
            raise ValueError(f"Use either a whole chapter or scenes for chapter {chapter}.")
        previous_order = (chapter_number, scene_number)
        if file_entry == "—":
            continue
        if not re.fullmatch(r"`[^`]+`", file_entry):
            raise ValueError(f"Expected an inline code path or an em dash at order {order}.")
        yield chapter_number, file_entry[1:-1]


def draft_body(file_entry):
    path = (ROOT / file_entry).resolve()
    if not path.is_relative_to(ROOT / "drafts") or path.suffix != ".md":
        raise ValueError(f"Draft path must refer to a Markdown file in drafts/: {file_entry}")
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if lines and lines[0] == "---":
        for index, line in enumerate(lines[1:], start=1):
            if line in {"---", "..."}:
                lines = lines[index + 1:]
                break
        else:
            raise ValueError(f"Unclosed YAML front matter in {file_entry}.")
    return "\n".join(lines).strip("\n")


def main():
    parts = []
    current_chapter = None
    try:
        for chapter, file_entry in index_rows():
            body = draft_body(file_entry)
            if not body.strip():
                continue
            parts.append(f"## Chapter {chapter}" if chapter != current_chapter else "* * *")
            parts.append(body)
            current_chapter = chapter
        if not parts:
            raise ValueError("No manuscript text is listed in INDEX.md.")
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1

    print("\n\n".join(parts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
