# Judging criteria for Website A vs Website B justifications

These criteria apply to pairwise website comparisons. In a **prompt task**, two websites
were built from the same written request. In a **clone task**, they were built from the
same reference image. The writing rules in section 3 apply to both.

## Contents
1. Task structure
2. What each question covers
3. Writing rules
4. Overall question
5. Calibration examples

## 1. Task structure

The input is a request (anything from one vague line to a detailed spec) and two
outputs, Website A and Website B. A clone task replaces the request with a reference
image.

Break the request down before judging:
- the app and its purpose
- the key features (sections, features and controls the request explicitly asks for)
- the visual direction (palette, fonts, layout style, image style, brands it mentions)

Visual direction informs the first question. Sections, features and behavior inform
Functionality.

How to inspect: scroll each page all the way down instead of judging the first screen,
click every control, and confirm that controls change the content instead of just being
present. If a website doesn't load, freezes, or renders too little to inspect, treat it
as not renderable and generally low quality.

On a prompt task, answer in this order: aesthetics, functionality, overall. Each answer
is one of: A is better, B is better, Both are good, Both are bad.

## 2. What each question covers

**Aesthetics (prompt task).** Judge everything visual:
- layout, composition, alignment and hierarchy
- typography and readability
- palette coherence, contrast, and respect for any requested palette
- gradients, glow, image quality and icon quality
- polish, consistency, spacing and density
- visual defects such as overlap, overflow, cut-off content and misalignment

The better-looking page can win, measured against the style the request asked for. A
page can win here even if none of its buttons work.

**Fidelity (clone task).** Judge with the same visual vocabulary, but against the
reference image. This compares three things: describe the reference, then what each
website kept, changed, dropped or added. Looking like the reference matters more than
looking good.

**Functionality and instruction following (prompt task).** This question has two parts:
- **Coverage.** The requested sections, features, content and data must be there. A site
  whose controls all work but which is missing half the requested sections fails.
- **Behavior.** The page loads without crashes, freezes or blank areas. Links, buttons,
  tabs, forms, filters and navigation respond and change the content. Nothing is dead or
  broken.

A control that exists is not the same as a control that works. A shell that looks
complete but isn't wired up fails.

A static page, such as a landing page or poster-style layout, still gets an answer. The
question becomes almost entirely about following the request, and the justification must
state that there is little or no behavior to test.

Ignore visual polish in this question. The one exception is rendering so broken that it
makes the page unusable, which counts as a functionality failure.

**Functionality (clone task).** Judge behavior only. On clone tasks, instruction
following does not belong in this field.

## 3. Writing rules

- **Author.** The annotator writes the text, with no LLM involvement of any kind.
  Grammar checkers are allowed. Each field should read naturally and reflect the
  annotator's own inspection.
- **Length.** Each field, counted on its own, must be 40 to 160 words.
- **Structure.** Lead with the verdict, then back it with concrete evidence about both
  websites.
- **Verdict first, matching the selection.**
  - For a win, open with "Website A is better because..." or "Website B is better
    because...".
  - For a tie, say it is a tie ("Website A and Website B are tied because..." or "...are
    both good because...") and make clear whether both are good or both are bad.
  - A list of points with no stated result does not count.
- **Keep to the field's lens.** No behavior in Aesthetics or Fidelity, and no
  appearance or resemblance in Functionality. Text that crosses lenses is wrong even if
  it is accurate. Only Overall may cover both.
- **Naming.** Always write "Website A" and "Website B".
  - Not allowed: bare letters ("A has...") and made-up labels (Site A, Page B, Option A,
    the first one, the left one).
  - Allowed: "both websites", "neither website", and pronouns that point to a website
    named in the same sentence or the one before.
- **Concrete details.** Point to differences that a reader could go and check.
- **Both websites.** Describe the loser too, not just the winner.
- **Report problems in the right field.** Breakage and dead controls go in
  Functionality. Visual defects and missing design elements go in the first field.
- **No category names.** Don't write "aesthetics", "functionality", "fidelity" or
  "instruction following". Describe what the sites look like and do.
- **Balanced ties.** A tie shouldn't list more faults for one website than the other.
- **No reused text** across the three fields.
- **Scope.** Write in the third person about the request and the two websites only.
  Don't mention the browser, browser tabs, refreshing, the platform, or "I".
- **Independence.** Each field must make sense when read on its own.

## 4. Overall question

Overall asks which website a real user would prefer to land on for this request. It
doesn't have to agree with either earlier answer, and it isn't calculated from them.

**When the two lenses disagree**, the justification must say which weakness hurts the
request more. Coverage and behavior usually weigh a bit more, but that is a tendency,
not a rule. A large visual gap can outweigh a small functional one. "Both are good" is
fine when each site is strong where the other is weak and neither clearly comes out
ahead.

**When the two lenses agree**, the justification explains what makes the combined result
clearly better instead of repeating one of the earlier answers.

Not allowed:
- automatically picking the Functionality winner
- repeating the Aesthetics answer
- reusing text from another justification
- covering only appearance, or only behavior

## 5. Calibration examples

**Bad: behavior in the aesthetics field.**
"Website A is better because it looks cleaner and its filter buttons update the listings,
while Website B has a search bar that does nothing."

**Good: a prompt-task set (brief, but each field keeps to its lens).**
- Aesthetics compares a consistent palette and even spacing against several clashing
  bright tones and hero text pressed against the image.
- Functionality compares filters that update the listings, with every requested section
  present, against a missing booking form and category tabs that never change the panel.
- Overall argues that one site's cleaner look doesn't make up for its missing booking
  form, because on the other site a traveller can actually search and reserve.

**Bad: overall that repeats functionality.**
"Website B is better because its navigation works and Website A does nothing when clicked."

**Bad: fidelity that never mentions the reference.**
"Website A is better because it looks cleaner and better organised than Website B."

**Annotated example: a generative poster request (prompt task).**
The request asks for a tool that draws a flower out of thin curves on a clean background,
with a few controls and an export button.
- Aesthetics is solid. It leads with the verdict, describes both sites, and gives
  checkable details (a scrollable settings sidebar, a centered labelled canvas, a
  generate button in the bottom-left corner). A control's position is a visual fact, so
  mentioning it here is fine.
- Functionality has a **lens problem**. Phrases like "clean white background", "smooth
  wave like curves", "airy negative space" and "no noise or blur" describe the requested
  *style*, which belongs in Aesthetics. This field should say whether each site actually
  draws the requested subject, whether each control (tone, scale, labels, export,
  generate) responds, and, because the request is mostly visual direction, that there is
  little behavior to test. Treating unrequested extras as neither a plus nor a minus is
  correct. Grammar: "wave like" needs a hyphen.
- Overall is good. It states that behavior is even and lets presentation decide, with a
  reason tied to the request (a poster-style piece). This makes the weighing visible.
