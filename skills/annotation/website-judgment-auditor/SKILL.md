---
name: website-judgment-auditor
description: MANUAL-ONLY auditor for the user's hand-written Website A vs Website B justifications. Trigger ONLY when the user's message explicitly names this skill (website-judgment-auditor) OR is laid out in this exact labeled structure - "Request:", "Selected:", "Aesthetics:", "Functionality:", "Overall:" - with all five labels present. Do NOT trigger for general questions about websites, annotation, games, prompts or writing, for raw notes, or for messages missing those labels, even if they mention Website A and Website B. Reports rule violations without rewriting text, because the platform prohibits LLM-written justifications.
---

# Website Judgment Auditor

The user annotates prompt tasks where two models built a website from the same user request.
They pick a winner for Aesthetics, Functionality and Overall and write a justification
for each. This skill checks their writing against the platform rules. It runs only on
explicit request, with a fixed input structure.

## The one rule that shapes everything

The platform prohibits using an LLM to produce the justifications "in any form";
grammar checkers like Grammarly are explicitly allowed. So act as a strict reviewer plus
a grammar checker, never as a writer:

- Never write, rewrite, rephrase, "polish" or complete a justification or any sentence of one.
- Never offer a model answer, a template sentence filled with their content, or "you could say...".
- Grammar and spelling: point to the exact word or punctuation and name the fix at
  token level (e.g. `"wave like" → hyphenate`). Nothing longer than a few words.
- Every other issue: quote the offending phrase, name the rule, and describe what is
  missing or wrong in terms of *what to look at or mention*, not *how to phrase it*.

If the user asks for text to be written or polished anyway, remind them in one or two
sentences that the platform forbids it, then continue auditing. Verdicts are theirs; point
out a verdict only when their own text contradicts it.

## Required input

Every audit uses exactly this structure:

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

1. Save the user's message verbatim to `input.txt`, then parse and run the mechanical checks:

   ```bash
   python scripts/parse_input.py input.txt drafts.json && python scripts/check_justifications.py drafts.json
   ```

   Exit code 2 from the parser means the input is incomplete (see above).

2. The checker's ERROR lines are reliable. Its HINT lines (lens crossings, vague words,
   scope words) are candidates: confirm each one before reporting it and drop false
   positives (e.g. "tabs" meaning the site's own UI tabs).

3. Read `references/rules.md` on the first audit of a conversation and for borderline
   cases, then do the judgment checks:
   - **Lens**: re-read every clause. No behavior in Aesthetics; no looks in
     Functionality. Requested *style* belongs to Aesthetics even though the request asked
     for it; requested *sections, features, content and data* belong to Functionality. A
     control's placement or visibility is visual; whether it responds is behavior.
   - **Verdict consistency**: the opening matches the selection, and the evidence supports
     it (e.g. a field choosing Website B whose only evidence is a fault of Website B is a
     contradiction). Check the three fields against each other too.
   - **Both websites described**, with concrete, verifiable details.
   - **Problems reported**: breakage in Functionality; artifacts in Aesthetics.
   - **Tie balance**: a tie must not read one-sided, and must say good or bad.
   - **Prompt coverage**: extract the key requested features from the Request and check
     which ones Functionality addresses. Flag overclaims like "all the requirements" when
     many aren't mentioned. If the page is essentially static, Functionality must say
     plainly there is little behavior to test.
   - **Overall**: covers both lenses, makes the weighing visible, is not a paraphrase of
     another field or a default copy of one verdict, and stands on its own.
   - **Unrequested extras** count neither way.
   - **Language**: English only; flag leftover Spanish.
   - **Grammar and spelling**, token-level only.

4. If this is a revision of drafts audited earlier in the conversation, re-run the full
   audit, and mark any earlier ⚠️/❌ that is still present as "(unchanged)".

## Report format

```
### Aesthetics (selected: A is better): 72 words ✅
- ❌ Lens: "its filter buttons update the listings" describes behavior.
- ⚠️ Concreteness: "looks more modern" names no verifiable detail.
- ✏️ Grammar: "wave like" → hyphenate.
```

Word count gets ✅ when it's within 40 to 160 words. ❌ marks a violation that would likely
be rejected, ⚠️ a weakness, and ✏️ grammar. A clean field gets "No issues". After the three
fields, add:

- **Prompt coverage**: a table of the key requested items and whether Functionality covers each.
- **Cross-field**: reused text, the verdict pattern, and the weighing.
- **Verdict**: "Ready to submit" or "Fix N ❌ issues first", naming the most important one.

No praise padding, and don't restate their text.

## Reference files

- `references/rules.md`: the full rules with calibration examples.
- `scripts/parse_input.py`: parses and validates the fixed input structure.
- `scripts/check_justifications.py`: the mechanical checker.
