# Build Log

Running log of what was done and why, in the order it happened. Same
format as the [ticket triage project's build
log](https://github.com/AzaRKazar/support-ticket-triage-llm-finetuning/blob/master/docs/build-log.md).

## 2026-08-17 — Project kickoff

Started while Project 2a (ticket triage) is blocked waiting on Azure GPU
quota approval — none of this project's early work (transcript gathering,
rubric design, labeling) needs GPU, so it's productive use of the wait
rather than sitting idle. Repo scaffolded, mirroring 2a's structure
(`.gitignore`, README with explicit exploratory-project framing per the
project brief — this one is intentionally not trying to look like a
production system).

One structural difference from 2a worth noting: `data/` is **not**
gitignored here. In 2a, data was regenerable from a public Hugging Face
dataset, so keeping it out of git was the right call. Here, the
hand-labeled data *is* the deliverable — the labeling process is the
point of the project — so it belongs in version control, visible and
reviewable.

## 2026-08-17 — Gathering earnings call transcripts

Pulled Q&A sections from 8 real Q2 2026 earnings calls (all public,
sourced from fool.com/earnings/call-transcripts, none paywalled): Wells
Fargo, Citi, Trade Desk, Expedia, AIG, Natera, Republic Airways, HSBC.
Chosen for sector spread (banking x3, adtech, travel, insurance,
healthcare diagnostics, airline) so the model sees varied language and
question styles rather than one industry's vocabulary.

**Data integrity was the main risk here, and it showed up in practice.**
The extraction tool (WebFetch, which runs page content through a
summarization model before returning it) repeatedly tried to compress or
paraphrase long answers instead of reproducing them verbatim, despite
explicit instructions not to -- this happened worst on Trade Desk, where
CEO Jeff Green's answers run unusually long. Two mitigations:

1. **Never trust the first pass.** Every extraction was spot-checked
   before saving -- looking for natural speech patterns (repeated words,
   filler language, run-on sentences) as a signal of genuine verbatim
   text versus the too-clean prose of a paraphrase.
2. **When bulk extraction failed, went granular.** For Trade Desk,
   whole-section and multi-exchange requests both came back
   summarized/ellipsis-compressed; only single-exchange requests
   produced genuinely complete text. That's expensive (one fetch per
   exchange), so rather than force it across ~20 exchanges, kept only
   the 3 that came back clean and accepted a smaller contribution from
   that company. Quality over hitting a per-company quota.

Also dropped, rather than patched over: one Citi exchange that cut off
mid-answer in the source ("[content truncated in source]" -- the tool
flagged this itself rather than inventing an ending, which is exactly
the behavior you want), and one HSBC exchange where the source didn't
have the question/answer content at all. Both are the kind of thing that
would be easy to silently paper over with a plausible-sounding fabrication
-- didn't.

One transcription mistake on my own end, worth logging rather than
hiding: the first attempt at writing up Wells Fargo's Q&A truncated
several answers shorter than what was actually extracted -- an ironic
failure given the whole point of the careful extraction prompting was
verbatim fidelity. Caught by comparing the written file against the
original tool output and rewrote it in full. Also missed one full
exchange (Ed Firth, KBW) when transcribing the HSBC extraction into its
file -- caught during the exchange-count tally and added back.

**Result:** 108 raw exchanges across the 8 transcripts (corrected --
see next entry). A handful of these are continuation answers (a second
executive adding detail to the same question rather than a new
question) that will get merged with their parent exchange during
labeling rather than counted twice. Per-file counts: Wells Fargo 22,
Citi 25, Natera 17, AIG 13, Expedia 12, HSBC 10, Republic Airways 6,
Trade Desk 3.

## 2026-08-17 — Caught a structural error in the Citi transcript

While building the labeling worksheet, re-reading the Citi file in full
(rather than trusting the earlier per-exchange count) surfaced a real
problem: the original extraction had bundled several follow-up questions
into the same speaker block as the executive's prior answer, with no
clean separation -- in one case (Ebrahim Poonawala's second question) a
new analyst question was sitting in the middle of a paragraph with no
speaker tag at all. The naive count of numbered items (15) was
undercounting real, distinct, labelable exchanges -- the actual number
was 25.

Restructured the file by hand, splitting every genuinely distinct
question into its own exchange while being careful this time to copy
full verbatim text (not repeat the earlier Wells Fargo truncation
mistake). Also caught and fixed two smaller slips introduced during that
rewrite: the CFO's name got mistyped as "Gonzalo Luqueño" instead of the
source's "Gonzalo Lucchetti" throughout, and one exchange's analyst got
mislabeled. Both fixed before committing.

**Why this matters for the project, not just as a bug fix:** this is
the kind of error that would have silently thrown away 10 real,
usable, hand-verified exchanges -- about 10% of the entire dataset --
if the exchange count hadn't been double-checked against the actual
file content rather than trusted from the first pass. Worth stating
plainly rather than quietly fixing: careful verification caught a real
problem here, twice in the same project now (see the earlier baseline
eval bug and the Wells Fargo truncation). That pattern is itself a
useful thing to be honest about in this project's process writeup.

Caught while building the labeling worksheet -- the labeling rubric
(below) was already written first, per the project's own rule that the
rubric has to come before any labeling-adjacent work solidifies.

## 2026-08-17 — Labeling rubric written

Wrote `docs/labeling-rubric.md` before any labeling began: Direct /
Partial / Evasive with an explicit decision procedure (list
sub-questions, check each was substantively addressed) rather than pure
gestalt judgment, edge-case guidance for the patterns that actually show
up in this data, and 6 worked examples pulled from the real gathered
transcripts -- including one borderline case shown with its resolution
rather than a clean one, since that's more useful for calibrating a
second rater than only showing easy cases.

Next: build a clean labeling worksheet from the (now-corrected)
transcripts, then hand off actual labeling -- that's explicitly the
user's work per the brief, not something to do on their behalf.

## 2026-08-17 — Labeling methodology: AI first pass, human review

Built `data/labeling_worksheet.csv` from the 8 transcripts via a script
(`src/build_worksheet.py`), not by hand -- 104 exchanges after merging
same-question continuation answers into their parent.

The original plan was for the user to hand-label all 104 from blank.
Partway into that, the user asked Claude to do the labeling instead.
Worth recording the actual conversation here rather than smoothing it
over: the initial answer was that doing so outright would undercut the
"self-labeled, demonstrates dataset-building skill" framing this whole
project is built on -- if every label were AI-generated with no human
judgment involved, the README's claims about the project wouldn't be
true anymore. The user then agreed to a middle path: Claude proposes a
label and reasoning for every exchange by applying the rubric's decision
procedure, and the user reviews and confirms or corrects each one,
rather than starting from a blank cell.

This isn't a euphemism for "AI labeled it and a human clicked accept" --
it's a real, disclosed methodology (`ai_proposed_label` /
`ai_reasoning` columns, kept separate from the human-owned `label`
column) that's honest about what happened at each step, which fits the
project's whole premise better than either pure-manual labeling (slower,
not actually different in kind from AI-assisted-and-reviewed) or
silent AI labeling (would make the README's framing false).

Applied via `src/apply_ai_labels.py` (104 labels, distribution: 53
Direct, 43 Partial, 7 Evasive, 1 flagged N/A -- exchange 78 is a
"thanks, guys" acknowledgment, not a real question, and got flagged for
likely exclusion rather than forced into a label).

Next: human review of all 104 proposed labels, then recruit a second
rater for the 20-30 sample and compute inter-rater agreement.

## 2026-08-17 — Human review of all 104 labels complete

Reviewed every AI-proposed label against the actual exchange text and
either confirmed or corrected it in the `label` column. Result: 10 of
104 changed (~90% agreement with the AI first pass) -- each change
came with a written reason citing the specific text, not just a
different gut call. Notably one change (id 74, the AIG premium-growth
positioning question) went the *stricter* direction, Partial -> Evasive,
which matters as evidence this was a real independent read rather than
a reflexive lean toward the more generous label.

One disagreement (id 56, Expedia/Andersen "what surprised you" question)
got pushed back on rather than accepted at face value: the note
justifying Direct actually described why the answer *doesn't* name a
surprise (expectations were confirmed, not upended), which argues for
keeping it at Partial. Left as an open item rather than resolved
unilaterally -- it's one row out of 104, not worth blocking on.

Built `data/rater2_blind_sample.csv`: 25 rows (`random.seed(42)`,
reproducible), sampled from the 103 real exchanges (id 78 excluded --
not a real question), stripped of `ai_proposed_label`, `ai_reasoning`,
and `label` entirely. This is the file an actual second person labels
independently. Showing them any prior label would defeat the purpose of
an inter-rater agreement check.

Next: find a second rater, have them label
`data/rater2_blind_sample.csv` against `docs/labeling-rubric.md`
without seeing anyone else's labels, then compute agreement.
