"""Report inconsistencies in explicit continuity annotations."""

from collections import defaultdict
from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
KEY = re.compile(r"[a-z][a-z0-9_-]*(?:\.[a-z0-9_-]+)+")
FRONT_MATTER = re.compile(r"\A---\n(.*?)^(?:---|\.\.\.)[ \t]*$", re.DOTALL | re.MULTILINE)
ANNOTATION = re.compile(r"^continuity_json:.*$", re.MULTILINE)
CANON_STATUS = re.compile(r"(['\x22]?)(locked|provisional|open_question)\1(?:[ \t]+#.*)?")


@dataclass
class Entry:
    source: str
    status: str
    facts: dict
    ages: list
    before: list


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key {key!r}.")
        result[key] = value
    return result


def year(value):
    return type(value) is int and value > 0


def read_entry(path, bible):
    text = path.read_text(encoding="utf-8-sig")
    frontmatter = FRONT_MATTER.match(text)
    if not frontmatter:
        if text.startswith("---\n") and ANNOTATION.search(text):
            raise ValueError("Unclosed front matter containing continuity_json.")
        return None
    header = frontmatter[1]
    blocks = list(ANNOTATION.finditer(header))
    if not blocks:
        return None
    if len(blocks) != 1 or blocks[0][0].strip() != "continuity_json: |":
        raise ValueError("Use one continuity_json: | field in front matter.")
    opening = blocks[0]
    json_lines = []
    for line in header[opening.end() + 1:].splitlines():
        if line and not line.startswith("  "):
            break
        json_lines.append(line)
    data = json.loads("\n".join(json_lines), object_pairs_hook=unique_object)
    if not isinstance(data, dict) or data.keys() - {"facts", "ages", "before"}:
        raise ValueError("Expected an object with optional facts, ages, and before keys.")
    facts, ages, before = data.get("facts", {}), data.get("ages", []), data.get("before", [])
    if not isinstance(facts, dict) or not isinstance(ages, list) or not isinstance(before, list):
        raise ValueError("facts must be an object. ages and before must be arrays.")
    for key, value in facts.items():
        scalar = (
            (isinstance(value, str) and bool(value.strip()))
            or type(value) is int
            or (type(value) is float and math.isfinite(value))
        )
        if not KEY.fullmatch(key) or not scalar:
            raise ValueError(f"Invalid fact key or value: {key!r}.")
        if key.endswith((".year", ".birth_year")) and not year(value):
            raise ValueError(f"{key} must be a positive integer year.")
    for item in ages:
        if (
            not isinstance(item, dict) or item.keys() != {"character", "year", "age"}
            or not isinstance(item["character"], str)
            or not re.fullmatch(r"[a-z][a-z0-9_-]*", item["character"])
            or not year(item["year"]) or type(item["age"]) is not int or item["age"] < 0
        ):
            raise ValueError("Each age needs a character ID, positive integer year, and nonnegative integer age.")
    for pair in before:
        if (
            not isinstance(pair, list) or len(pair) != 2
            or any(not isinstance(key, str) or not KEY.fullmatch(key)
                   or not key.startswith("event.") or not key.endswith(".year") for key in pair)
            or pair[0] == pair[1]
        ):
            raise ValueError("Each before pair needs two distinct event.*.year keys.")

    status = "draft"
    if bible:
        fields = re.findall(r"^canon_status:[ \t]*(.*)$", header, re.MULTILINE)
        match = CANON_STATUS.fullmatch(fields[0].strip()) if len(fields) == 1 else None
        if not match:
            raise ValueError("An annotated Story Bible entry needs one recognized canon_status in front matter.")
        status = match[2]
    line = header.count("\n", 0, opening.start()) + 2
    return Entry(f"{path.relative_to(ROOT)}:{line}", status, facts, ages, before)


def fact_index(entries):
    index = defaultdict(list)
    for entry in entries:
        for key, value in entry.facts.items():
            index[key].append((value, entry.source))
    return index


def agreed(claims):
    return bool(claims) and all(value == claims[0][0] for value, _ in claims)


def evidence(claims):
    return ", ".join(f"{value!r} at {source}" for value, source in claims)


def compare_facts(locked, drafts, findings):
    for key, claims in sorted(locked.items()):
        if not agreed(claims):
            findings["Review"].append(f"Locked sources disagree on `{key}`: {evidence(claims)}.")
    for key, claims in sorted(drafts.items()):
        baseline = locked.get(key, [])
        if agreed(baseline):
            for value, source in claims:
                if value != baseline[0][0]:
                    findings["Locked canon mismatch"].append(
                        f"`{key}` is {value!r} at {source}. Locked value is {evidence(baseline)}."
                    )
        elif not baseline:
            findings["Coverage"].append(f"No locked reference for `{key}` ({claims[0][1]}).")
        if not agreed(claims):
            findings["Review"].append(f"Drafts disagree on `{key}`: {evidence(claims)}.")


def check_ages(entries, reference, locked, findings):
    for entry in entries:
        for item in entry.ages:
            key = f"character.{item['character']}.birth_year"
            baseline = locked.get(key, [])
            birth = baseline if agreed(baseline) else reference.get(key, [])
            if not agreed(baseline) and key in entry.facts:
                birth = [(entry.facts[key], entry.source)]
            if not agreed(birth):
                findings["Coverage"].append(f"Cannot check age at {entry.source} without an agreed `{key}`.")
                continue
            difference = item["year"] - birth[0][0]
            if item["age"] not in (difference - 1, difference):
                label = "Locked canon mismatch" if agreed(baseline) else "Review"
                findings[label].append(
                    f"{item['character']} is listed as age {item['age']} in {item['year']} at "
                    f"{entry.source}, which is incompatible with birth year {evidence(birth)}."
                )


def check_chronology(entries, reference, findings, *, only_with=None):
    for entry in entries:
        for first, second in entry.before:
            if only_with is not None and first not in only_with and second not in only_with:
                continue
            earlier, later = reference.get(first, []), reference.get(second, [])
            if not agreed(earlier) or not agreed(later) or earlier[0][0] == later[0][0]:
                findings["Coverage"].append(
                    f"Cannot establish `{first}` before `{second}` at {entry.source} "
                    "(missing, conflicting, or same-year dates)."
                )
            elif earlier[0][0] > later[0][0]:
                findings["Review"].append(
                    f"Reversed chronology for `{first}` before `{second}` at {entry.source}: "
                    f"{evidence(earlier)} versus {evidence(later)}."
                )


def main():
    locked, drafts = [], []
    skipped, scanned = 0, 0
    findings = {"Input problem": [], "Locked canon mismatch": [], "Review": [], "Coverage": []}
    for folder, bible in (("01-story-bible", True), ("04-manuscript/drafts", False)):
        for path in sorted((ROOT / folder).rglob("*.md")):
            scanned += 1
            try:
                entry = read_entry(path, bible)
            except (OSError, ValueError) as error:
                findings["Input problem"].append(f"{path.relative_to(ROOT)}: {error}")
                continue
            if entry is None:
                continue
            if entry.status == "locked":
                locked.append(entry)
            elif entry.status == "draft":
                drafts.append(entry)
            else:
                skipped += 1

    locked_facts, draft_facts = fact_index(locked), fact_index(drafts)
    compare_facts(locked_facts, draft_facts, findings)
    draft_reference = locked_facts | draft_facts
    check_ages(locked, locked_facts, {}, findings)
    check_ages(drafts, draft_reference, locked_facts, findings)
    check_chronology(locked, locked_facts, findings)
    check_chronology(drafts, draft_reference, findings)
    check_chronology(locked, draft_reference, findings, only_with=draft_facts)

    print("# Continuity report\n")
    print(f"Scanned {scanned} Markdown files. Found {len(locked)} annotated locked entries, "
          f"{len(drafts)} annotated drafts, and {skipped} non-locked annotated Story Bible entries.")
    if not locked:
        print("\nNo annotated locked canon is available for comparison.")
    if not drafts:
        print("\nNo annotated manuscript drafts are available for comparison.")
    for label, messages in findings.items():
        print(f"\n## {label} ({len(messages)})\n")
        print("\n".join(f"- {message}" for message in messages) if messages else "None.")
    return int(any(findings[label] for label in ("Input problem", "Locked canon mismatch", "Review")))


if __name__ == "__main__":
    sys.exit(main())
