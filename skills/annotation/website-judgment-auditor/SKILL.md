---
name: website-judgment-auditor
description: MANUAL-ONLY auditor for the user's hand-written Website A vs Website B justifications. Trigger ONLY when the user's message explicitly names this skill (website-judgment-auditor) OR is laid out in this exact labeled structure - "Request:", "Selected:", "Aesthetics:", "Functionality:", "Overall:" - with all five labels present. Do NOT trigger for general questions about websites, annotation, games, prompts or writing, for raw notes, or for messages missing those labels, even if they mention Website A and Website B. Audits against an injected rules file and reports violations without rewriting text, because the platform prohibits LLM-written justifications.
---

# Website Judgment Auditor

The user annotates tasks where two models built a website from the same request. They pick a
winner for Aesthetics, Functionality and Overall and write a justification for each. This skill
checks their writing against the project rules. It runs only on explicit request, with a fixed
input structure.

## The project rules are injected

This skill ships no rules. They are supplied as a separate rules file when the skill is
initialized, expected at `references/rules.md` (never commit a local copy). Read it before
auditing and treat it as the only source of truth: limits, naming, lenses, verdict format,
everything. If no rules file is present, stop and ask the user to provide one. Do not audit
from memory.

## The one rule that shapes everything

The platform prohibits using an LLM to produce the justifications "in any form";
grammar checkers are explicitly allowed. So act as a strict reviewer plus a grammar
checker, never as a writer:

- Never write, rewrite, rephrase, "polish" or complete a justification or any sentence of one.
- Never offer a model answer, a template sentence filled with their content, or "you could say...".
- Grammar and spelling: point to the exact word or punctuation and name the fix at
  token level. Nothing longer than a few words.
- Every other issue: quote the offending phrase, name the rule it breaks, and describe what is
  missing or wrong in terms of *what to look at or mention*, not *how to phrase it*.

If the user asks for text to be written or polished anyway, remind them in one or two
sentences that the platform forbids it, then continue auditing. Verdicts are theirs; point
out a verdict only when their own text contradicts it.

## Required input

```
Request: [user request, any length]
Selected: Aesthetics A, Functionality both good, Overall A
Aesthetics: [draft]
Functionality: [draft]
Overall: [draft]
```

Choices on the `Selected:` line are `A`, `B`, `both good`, or `both bad`.

If a label is missing, empty, or a choice is unrecognized, do not audit. Reply with the
parser's list of problems and show the template above so they can resend. Do not guess
missing selections from the drafts.

## Workflow

1. Save the user's message verbatim to `input.txt`, then parse it:

   ```bash
   python scripts/parse_input.py input.txt drafts.json
   ```

   Exit code 2 means the input is incomplete (see above).

2. Read the injected rules file, then check every field of `drafts.json` against it, including
   consistency between each draft and its selection, and across the three fields.

3. If this is a revision of drafts audited earlier in the conversation, re-run the full
   audit, and mark any earlier ⚠️/❌ that is still present as "(unchanged)".

## Report format

```
### Aesthetics (selected: A is better): N words
- ❌ <rule>: "<quoted phrase>" <what is wrong>.
- ⚠️ <rule>: "<quoted phrase>" <weakness>.
- ✏️ Grammar: "<word>" → <token-level fix>.
```

❌ marks a violation that would likely be rejected, ⚠️ a weakness, ✏️ grammar. Mark the word
count ✅ or ❌ per the rules file's limits. A clean field gets "No issues". After the three
fields, add:

- **Cross-field**: issues that span fields, such as reused text or verdict pattern.
- **Verdict**: "Ready to submit" or "Fix N ❌ issues first", naming the most important one.

No praise padding, and don't restate their text.

## Files

- `scripts/parse_input.py`: parses and validates the fixed input structure.
- `references/rules.md`: the project rules, injected at initialization.
