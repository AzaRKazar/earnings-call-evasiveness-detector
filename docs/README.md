# Project Documentation

Consolidated explainer for the labeling methodology and results. For the
chronological, as-it-happened account, see [`build-log.md`](build-log.md).

## The task

Classify analyst Q&A exchanges from real earnings calls as **Direct**,
**Partial**, or **Evasive** — see [`labeling-rubric.md`](labeling-rubric.md)
for the full decision procedure and worked examples.

## Dataset

104 exchanges from 8 real Q2 2026 earnings calls (Wells Fargo, Citi,
Trade Desk, Expedia, AIG, Natera, Republic Airways, HSBC), gathered and
verified for verbatim accuracy — see `build-log.md` for the data-quality
issues that came up during extraction and how they were handled.

## Labeling methodology

**AI-assisted first pass, human-reviewed.** Claude proposed a label and
one-sentence reasoning for every exchange by applying the rubric's
decision procedure. A human then read every exchange independently and
confirmed or corrected each one — 10 of 104 (~90% agreement with the
first pass) were changed after re-reading the actual text, one of them
in the *stricter* direction, which is evidence this was genuine review
rather than rubber-stamping. This is disclosed as the actual process
rather than framed as unassisted manual labeling.

**Final label distribution (all 104):**

| Label | Count |
|---|---|
| Direct | 62 |
| Partial | 33 |
| Evasive | 8 |
| N/A (excluded — not a real question) | 1 |

## Inter-rater agreement

A second person, independent of the primary labeling process, labeled a
blind 25-example sample (`data/rater2_blind_sample.csv`, `random.seed(42)`)
against the same rubric, with no visibility into the primary labels, the
AI proposals, or any reasoning — only the raw question/answer text.

| Metric | Value |
|---|---|
| Raw agreement | 17/25 (68.0%) |
| **Cohen's kappa** | **0.375** |

**Read this honestly, not optimistically.** 68% sounds passable on its
own, but Cohen's kappa corrects for the agreement you'd expect from
chance alone — and with Direct as the majority class in this dataset,
two raters both leaning toward the common label inflates raw agreement
without reflecting real convergent judgment. 0.375 falls in the "fair"
range on the standard Landis & Koch scale (0.21–0.40), below "moderate"
(0.41–0.60). This is a real result, not a strong one, and it's reported
as such rather than only quoting the friendlier raw percentage.

**Where the disagreement actually lives, and why that matters:** all 8
disagreements were adjacent-category (Direct↔Partial or Partial↔Evasive)
— zero were Direct↔Evasive, the two extremes. And 7 of the 8 cluster
specifically at the Direct/Partial boundary. That's not noise; it's a
coherent signal that the genuinely hard judgment call in this task is
"did the answer *fully* address every part of the question, or just
*most* of it" — exactly the multi-part-question ambiguity the rubric
tries to handle explicitly, and evidently doesn't fully resolve even
with a written decision procedure in front of both raters. A follow-up
rubric revision narrowing that specific boundary (e.g., a stricter rule
for how much of a compound question can go unaddressed before it drops
out of Direct) would be the concrete next step if this dataset were
being extended, rather than a vague "improve consistency" gesture.

## What this does and doesn't support

This sample (25 exchanges) and this kappa are not grounds for strong
claims about the rubric's reliability at scale. What it *does* support:
a specific, falsifiable description of where two careful readers applying
the same written rubric diverge, and a reasonable prior that the
Direct/Partial line is softer than the rubric's prose suggests. That's
the honest scope of what a 25-example inter-rater check can tell you,
and overstating it would undercut the exact thing this project is meant
to demonstrate.
