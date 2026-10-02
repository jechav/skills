#!/usr/bin/env python3
"""Mechanical checks for Website A vs Website B justifications.

Usage: python check_justifications.py drafts.json

drafts.json:
{
  "task_type": "prompt" | "clone",
  "selected": {"first": "A|B|tie_good|tie_bad", "functionality": ..., "overall": ...},
  "texts":    {"first": "...", "functionality": "...", "overall": "..."}
}
"first" = Aesthetics (prompt task) or Fidelity (clone task).

Hard checks (ERROR) are reliable. HINT lines are candidates for the model to confirm.
"""
import json
import re
import sys

MIN_WORDS, MAX_WORDS = 40, 160

BEHAVIOR_WORDS = [
    r"click(?:s|ed|ing)?", r"works?", r"working", r"respond(?:s|ed)?", r"updat(?:e|es|ed|ing)",
    r"functional", r"does nothing", r"do nothing", r"dead", r"load(?:s|ed|ing)?", r"navigat\w*",
    r"submit\w*", r"filter(?:s|ed|ing)?", r"export(?:s|ed)?", r"download\w*", r"generat(?:e|es|ed)",
    r"toggle\w*", r"interactive", r"crash\w*", r"freez\w*", r"leads? nowhere", r"wired",
]
VISUAL_WORDS = [
    r"colou?rs?", r"palette", r"fonts?", r"typograph\w*", r"spacing", r"padding", r"margins?",
    r"beautiful", r"elegant", r"clean(?:er)?", r"polish\w*", r"sharp(?:er)?", r"blur\w*", r"noise",
    r"background", r"gradients?", r"glow", r"align\w*", r"contrast", r"whitespace", r"white space",
    r"negative space", r"looks?", r"visual\w*", r"attractive", r"stylish", r"modern", r"layout",
    r"centered", r"centred", r"cramped", r"crowd\w*",
]
VAGUE_PHRASES = [
    r"looks? (?:better|nicer|good|great|cleaner|more \w+)", r"more (?:polished|professional|modern|appealing)",
    r"better overall", r"feels? (?:better|nicer|more \w+)", r"overall better", r"nicer",
    r"more complete", r"works better", r"better design", r"better experience",
]
CATEGORY_WORDS = [r"aesthetics?", r"functionality", r"fidelity", r"instruction[- ]following"]
SCOPE_WORDS = [
    r"browser", r"new tab", r"this tab", r"the other tab", r"browser tab", r"refresh\w*",
    r"platform", r"annotat\w*", r"the task", r"the form", r"screenshot",
]
FIRST_PERSON = [r"\bI\b", r"\bI'm\b", r"\bI've\b", r"\bmy\b", r"\bme\b", r"\bwe\b", r"\bour\b"]
INVENTED_LABELS = [
    r"\b(?:site|page|option|version|candidate|model|output|design|app)\s+[AB]\b",
    r"\b(?:first|second|left|right) one\b", r"\bthe former\b", r"\bthe latter\b",
    r"\bweb\s?site\s+(?:one|two|1|2)\b",
]
SPANISH_HINTS = [r"\b(?:el|la|los|las|pero|porque|muy|también|mejor|sitio|página)\b"]


def words(t):
    return re.findall(r"[A-Za-z0-9'’-]+", t)


def find(patterns, text, flags=re.IGNORECASE):
    hits = []
    for p in patterns:
        for m in re.finditer(r"\b" + p + r"\b" if not p.startswith(r"\b") else p, text, flags):
            start = max(0, m.start() - 30)
            hits.append((m.group(0), text[start:m.end() + 30].replace("\n", " ")))
    return hits


def bare_letters(text):
    hits = []
    for m in re.finditer(r"\b([AB])\b", text):
        before = text[max(0, m.start() - 8):m.start()]
        if re.search(r"(?i)(Website|site|page|option|version|candidate|model|output|design|app)\s$", before):
            continue  # full name, or an invented label reported separately
        letter = m.group(1)
        at_sentence_start = re.search(r"(^|[.!?]\s+|\n)$", text[:m.start()])
        if letter == "A" and at_sentence_start:
            nxt = text[m.end():m.end() + 8]
            if not re.match(r"\s*(?:is|has|was|and|or|,|'s|’s|keeps|shows|uses)\b", nxt):
                continue  # article "A"
        hits.append(text[max(0, m.start() - 25):m.end() + 25].replace("\n", " "))
    return hits


def check_opening(text, sel):
    first = re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0]
    if sel in ("A", "B"):
        if not re.match(rf"Website {sel} is better because", first):
            other = "B" if sel == "A" else "A"
            if re.match(rf"Website {other} is better", first):
                return f"ERROR opening names Website {other} but selection is {sel}"
            return f"ERROR should open with 'Website {sel} is better because...' | got: {first[:80]!r}"
    elif sel in ("tie_good", "tie_bad"):
        if not re.match(r"(Website A and Website B|Both websites|Neither website)", first):
            return f"ERROR tie should open by naming the tie ('Website A and Website B ...') | got: {first[:80]!r}"
        if re.match(r"Website [AB] is better", first):
            return "ERROR opening declares a winner but a tie was selected"
        good = re.search(r"\b(good|strong|well|both deliver|succeed)", first, re.I)
        bad = re.search(r"\b(bad|weak|poor|fail|broken|neither)", first, re.I)
        want = "good" if sel == "tie_good" else "bad"
        if (want == "good" and bad and not good) or (want == "bad" and good and not bad):
            return f"ERROR tie opening reads as the wrong kind of tie (selected: both {want})"
        if not (good or bad):
            return f"WARN tie opening doesn't make clear whether the pair is {want}"
    else:
        return f"WARN unknown selection {sel!r}"
    return None


def ngrams(text, n=6):
    w = [x.lower() for x in words(text)]
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def main(path):
    data = json.load(open(path, encoding="utf-8"))
    task = data.get("task_type", "prompt")
    names = {"first": "Aesthetics" if task == "prompt" else "Fidelity",
             "functionality": "Functionality", "overall": "Overall"}
    texts, sel = data["texts"], data["selected"]

    for key, label in names.items():
        t = texts.get(key, "") or ""
        wc = len(words(t))
        print(f"\n=== {label} (selected: {sel.get(key)}) — {wc} words ===")
        if wc < MIN_WORDS:
            print(f"ERROR too short: {wc} < {MIN_WORDS}")
        elif wc > MAX_WORDS:
            print(f"ERROR too long: {wc} > {MAX_WORDS}")
        if re.match(r"\s*overall\b", t, re.I):
            print("ERROR opens with the category word 'Overall'; start with the website name")
        op = check_opening(t, sel.get(key))
        if op:
            print(op)
        if "Website A" not in t or "Website B" not in t:
            if not re.search(r"\b(both|neither) websites?\b", t, re.I):
                print("WARN only one website is named; describe both")
        for h in bare_letters(t):
            print(f"ERROR bare letter: ...{h}...")
        for m in re.finditer(r"\b(?:website|WEBSITE|Web site|web site)\s+[AB]\b", t):
            print(f"ERROR lowercase or variant name {m.group(0)!r}: write 'Website A' / 'Website B'")
        for w, ctx in find(INVENTED_LABELS, t):
            print(f"ERROR invented label {w!r}: ...{ctx}...")
        for w, ctx in find(CATEGORY_WORDS, t):
            print(f"ERROR names an evaluation category {w!r}: ...{ctx}...")
        for w, ctx in find(SCOPE_WORDS, t):
            print(f"HINT out-of-scope word {w!r}: ...{ctx}...")
        for w, ctx in find(FIRST_PERSON, t, flags=0):
            print(f"ERROR first person {w!r}: ...{ctx}...")
        for w, ctx in find(SPANISH_HINTS, t):
            print(f"HINT possible Spanish {w!r}: ...{ctx}...")
        if key == "first":
            for w, ctx in find(BEHAVIOR_WORDS, t):
                print(f"HINT possible behavior in visual field {w!r}: ...{ctx}...")
        if key == "functionality":
            for w, ctx in find(VISUAL_WORDS, t):
                print(f"HINT possible looks in behavior field {w!r}: ...{ctx}...")
        if key == "overall":
            has_b = bool(find(BEHAVIOR_WORDS, t)) or re.search(r"request|asked|missing|present", t, re.I)
            has_v = bool(find(VISUAL_WORDS, t))
            if not (has_b and has_v):
                print("HINT overall may cover only one lens (check it weighs both)")
        for w, ctx in find(VAGUE_PHRASES, t):
            print(f"HINT vague phrase {w!r} (is a verifiable detail given?): ...{ctx}...")

    print("\n=== Cross-field ===")
    keys = list(names)
    found = False
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            shared = ngrams(texts.get(keys[i], "")) & ngrams(texts.get(keys[j], ""))
            if shared:
                found = True
                print(f"ERROR reused text between {names[keys[i]]} and {names[keys[j]]}: "
                      + "; ".join(sorted(shared)[:3]))
    if not found:
        print("OK no reused 6-word runs")
    s = sel
    if s.get("overall") == s.get("functionality") and s.get("overall") != s.get("first"):
        print("HINT overall matches Functionality and differs from the first field: make sure the weighing is explained, not defaulted")
    if s.get("overall") not in (s.get("first"), s.get("functionality")):
        print("HINT overall differs from both other verdicts: valid, but the justification must explain why")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
