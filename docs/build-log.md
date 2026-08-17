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
