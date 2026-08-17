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

**Result:** 98 raw exchanges across the 8 transcripts. A handful of
these are continuation answers (a second executive adding detail to the
same question rather than a new question) that will get merged with
their parent exchange during labeling rather than counted twice -- real
distinct-question count is in the low-to-mid 90s, just under the brief's
~100-150 target but close enough not to chase further. Per-file counts:
Wells Fargo 22, Citi 15, Natera 17, AIG 13, Expedia 12, HSBC 10, Republic
Airways 6, Trade Desk 3.

Next: write the labeling rubric before labeling any of this.
