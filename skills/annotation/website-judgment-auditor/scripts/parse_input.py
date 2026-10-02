#!/usr/bin/env python3
"""Parse the fixed audit input format into the JSON the checker expects.

Usage: python parse_input.py input.txt drafts.json

Expected input (labels are case-insensitive, each starts a line):
Request: ...            (may span many lines)
Selected: Aesthetics A, Functionality both good, Overall A
Aesthetics: ...
Functionality: ...
Overall: ...

Exits with code 2 and prints what is missing or malformed if the input is incomplete.
"""
import json
import re
import sys

LABELS = ["request", "selected", "aesthetics", "functionality", "overall"]
LABEL_RE = re.compile(r"^\s*\**\s*(request|selected|aesthetics|functionality|overall)\s*\**\s*:\s*",
                      re.IGNORECASE | re.MULTILINE)


def norm_choice(raw):
    r = raw.strip().lower().rstrip(".")
    r = re.sub(r"^website\s+", "", r)
    r = re.sub(r"\s+is better$", "", r)
    if r in ("a", "b"):
        return r.upper()
    if re.fullmatch(r"(both|tie)[\s_-]*(are\s+)?good", r):
        return "tie_good"
    if re.fullmatch(r"(both|tie)[\s_-]*(are\s+)?bad", r):
        return "tie_bad"
    return None


def parse_selected(line):
    out, problems = {}, []
    for key in ("aesthetics", "functionality", "overall"):
        m = re.search(rf"{key}\s*[:=]?\s*([^,;\n]+)", line, re.IGNORECASE)
        if not m:
            problems.append(f"Selected line has no choice for {key.title()}")
            continue
        choice = norm_choice(m.group(1))
        if not choice:
            problems.append(f"Unrecognized choice for {key.title()}: {m.group(1).strip()!r} "
                            "(use A, B, both good, or both bad)")
        else:
            out[key] = choice
    return out, problems


def main(src, dst):
    text = open(src, encoding="utf-8").read()
    parts, matches = {}, list(LABEL_RE.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        key = m.group(1).lower()
        if key in parts:
            print(f"DUPLICATE label {key.title()}: (first one kept)")
            continue
        parts[key] = text[m.end():end].strip()

    problems = [f"MISSING {k.title()}:" for k in LABELS if not parts.get(k)]
    selected = {}
    if parts.get("selected"):
        selected, sel_problems = parse_selected(parts["selected"])
        problems += sel_problems
    if problems:
        print("INPUT INCOMPLETE")
        for p in problems:
            print("- " + p)
        sys.exit(2)

    data = {
        "task_type": "prompt",
        "request": parts["request"],
        "selected": {"first": selected["aesthetics"], "functionality": selected["functionality"],
                     "overall": selected["overall"]},
        "texts": {"first": parts["aesthetics"], "functionality": parts["functionality"],
                  "overall": parts["overall"]},
    }
    json.dump(data, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"OK parsed -> {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
