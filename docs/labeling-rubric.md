# Labeling Rubric: Direct / Partial / Evasive

Written before any labeling began, per the project's own rule for this
kind of self-labeled task — the rubric has to come first, or it just
becomes a post-hoc justification for gut reactions.

## What's being judged

Each labeled unit is one **exchange**: an analyst's question (which may
have multiple sub-questions bundled into it — very common in these
calls) and the executive's complete response to it.

The question being answered by the label is narrow and specific:

> **Did the executive's answer substantively address what was actually
> asked?**

This is a judgment about **responsiveness**, not about:
- Whether the answer is *true*. Raters usually have no way to verify
  that, and it's a different question from whether the question was
  engaged with.
- Whether the news is good or bad. A direct "no" or "we missed the
  target" is Direct. A cheerful non-answer is still not an answer.
- Length. Long and short answers can both be Direct or Evasive — see
  below.

## The three categories

**Direct** — every distinct part of the question gets a substantive,
specific response: a number where a number was asked for, a clear
stance where a stance was asked for, a concrete explanation where one
was asked for.

**Partial** — at least one distinct part of the question gets a
substantive response, but at least one other clearly-asked part is
dropped, deflected, or answered only in vague generalities.

**Evasive** — no part of the question receives a substantive, specific
response. The answer changes the subject, restates prepared talking
points that don't engage the actual ask, or explicitly declines to
answer without addressing the rest of the question either.

## Decision procedure

1. **List the distinct sub-questions.** Many of these questions are
   compound ("First X... and then second, Y..."). Write down what's
   actually being asked before reading the answer.
2. **For each sub-question, ask: did the answer give a specific,
   responsive fact, number, or stance — or only topic-adjacent
   commentary?**
3. **Apply the mapping:** all sub-questions substantively addressed →
   Direct. Some addressed, some not → Partial. None addressed → Evasive.
4. **Check the edge cases below before finalizing** — most disagreements
   will come from these, not from the basic definitions.

## Edge cases (read these before labeling)

### Multi-part questions where only part gets answered

This is the single most common pattern in the data, and the reason
Partial exists as a category rather than forcing a binary choice. Judge
each distinct part separately per the decision procedure above — don't
average an overall "vibe." One clearly-dodged part is enough to keep an
otherwise-thorough answer out of Direct.

### Legitimate, explicit non-disclosure

Executives sometimes have a real reason not to answer — confidentiality
about a specific partner, forward-looking guidance policy, ongoing
litigation. Treat an **explicit, reasoned** declination ("we don't
comment on individual partners") differently from a **deflection that
pretends to engage** while dodging. A clean explicit non-disclosure on
one part of a question, combined with a real answer on the rest, is
Partial, not Evasive — the executive was at least honest about not
answering rather than obscuring it. See Worked Example 4 below.

### Long, hedging, but ultimately substantive answers

Most answers in this dataset open with throat-clearing ("great
question," "let me start by saying") and include a lot of qualifying
language. Don't penalize this. Find the substantive content, if any, and
judge based on that relative to what was asked — not based on how much
verbal padding surrounds it.

### Restating prior guidance instead of engaging a new ask

A common pattern: analyst asks for something new (a specific number, a
change in outlook) and the executive responds by re-confirming
previously-given guidance almost verbatim. This can go either way:
- If the question was literally "has this changed?" and the answer is
  "no, unchanged, here's why" — that's **Direct**.
- If the question asked for something the prior guidance didn't cover
  (new specifics, a forward-looking commitment) and the answer just
  repeats the old talking point without engaging the new part — that's
  **Evasive** on that part. See Worked Example 6.

### Watch for length as camouflage

Genuinely evasive answers are rarer in this data than you might expect
going in — these are practiced communicators, and full stonewalling is
uncommon. What's much more common is a long, detailed, confident-sounding
answer that never actually lands on the specific thing asked. Don't let
volume or fluency substitute for checking: is there an actual number,
fact, or stance here that responds to the question? If you have to
paraphrase generously to make the answer "count," it's probably Partial
or Evasive, not Direct.

## Worked examples (from the actual dataset)

### Example 1 — Direct
*Republic Airways, Michael Linenberg → Joe Allman (CFO)*

> **Q:** "Can you just remind us... your percentages of what you own of
> Eve and Cape Air?"
>
> **A:** "We're about a 40% owner in the Cape Air equity. And on the Eve
> investment, that's really a mark-to-market on the warrants that we
> hold related to Eve that flows through the non-operating line."

**Direct.** Specific number for the first part (40%), and a clear,
concrete explanation of why the second part doesn't reduce to a simple
percentage. Both parts substantively addressed.

### Example 2 — Direct
*AIG, Rowland Mayor → Keith Walsh (CFO)*

> **Q:** "...if in your fixed income portfolio, you're starting to have
> significant allocations to AI-related corporate debt."
>
> **A:** "We don't have significant allocations to AI-specific related
> debt... direct software exposure, for example, is 16 basis points of
> the portfolio. So I would say any of these allocations are pretty
> immaterial at this point."

**Direct.** A specific, quantified, unhedged answer to a yes/no-shaped
question, with a real number attached.

### Example 3 — Partial
*Wells Fargo, Erika Najarian → Michael Santomassimo (CFO)*

> **Q (second half of a longer question):** "...maybe describe a little
> bit more the prime financing opportunity that lies ahead, especially
> if the sort of traditional counterparties have more limited capacity
> because of activities outside of The US."
>
> **A (excerpt):** "...what we have found is that people want more
> options... We are still very, very early in terms of growing out our
> prime business. So there is nothing really material in this current
> quarter relative to that..."

**Partial.** The first half of the compound question (investment
banking pipeline) got a specific, confident answer elsewhere in the same
response. This half — the actual prime financing opportunity being
asked about — gets only "nothing material" and general reassurance, no
figures or specifics despite the question explicitly inviting them.

### Example 4 — Partial (legitimate non-disclosure)
*Expedia, Naved Khan → Ariane Gorin (CEO)*

> **Q:** "...any early read or any color you can share in terms of how
> [the Uber partnership] is rolling out, and what are you contemplating
> in your guidance in terms of contribution from this new partnership?"
>
> **A (excerpt):** "I'll take the second one first because it's going to
> be quick, which is we don't comment on individual partners. I'm not
> going to comment, and it's not going to be material to our guidance."

**Partial**, not Evasive — this is the "legitimate non-disclosure" edge
case. The executive is explicit and honest about not answering (rather
than pretending to), and the same response goes on to substantively
answer the other half of the compound question (attach rates) in detail.

### Example 5 — Evasive
*HSBC, Amit Goel (follow-up) → Georges Elhedery (CEO)*

> **Q:** "...does that mean that the following year, so 2028, we would
> expect to see a drop-down in that investment spend? Or do we just see
> that continuing beyond '27?"
>
> **A:** "We're not giving guidance actually for '27 or '28... these are
> investments along our strategic priorities that have been very much
> earmarked... this is really what we mean is bringing forward some of
> this investment plan..."

**Evasive.** This is a narrow, specific, answerable-in-principle
question (does spending step down or not, after the acceleration
period?) and the response explicitly declines to answer it, then
substitutes generic strategic reassurance that doesn't engage the actual
timing question at all.

### Example 6 — borderline, and how it was resolved
*Expedia, Kevin Kopelman → Ariane Gorin (CEO)*

> **Q:** "Could you just give us some more color on how you've seen U.S.
> and Mexico trips progress as we've gotten further away from the
> security incident that you called out last quarter?"
>
> **A (complete):** "Yeah. I would say we've seen a normalization. Yeah.
> We've seen a normalization."

This one is genuinely borderline and worth showing rather than hiding.
**Resolved as Partial.** It does make a clear, specific claim
("normalized") that directly answers the literal question — that pushes
toward Direct. But the question explicitly asked for "more color," and
the answer gives none: no numbers, no timeline, no explanation of what
normalization looks like. Repeating the one-word claim instead of
elaborating reads as minimizing engagement with a question about a past
negative event, not as genuine full disclosure. If you hit a case like
this, lean Partial and note it — don't force it into Direct just because
a literal claim was made.

## What to do when you're genuinely unsure

Label your best judgment, but flag the exchange (a `notes` column, not a
separate label) with a short reason. Disagreements concentrated on
flagged exchanges are expected and fine to report as such — that's a
finding, not a failure of the rubric. Disagreement spread evenly across
easy and hard cases would be the actual red flag.
