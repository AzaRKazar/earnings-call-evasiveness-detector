# Earnings Call Evasiveness Detector

> **Exploratory project.** This is a small dataset (104 examples) built
> from scratch and labeled with an AI-assisted-first-pass, human-reviewed
> workflow, fine-tuned with the same QLoRA approach as the [ticket triage
> project](https://github.com/AzaRKazar/support-ticket-triage-llm-finetuning).
> Metrics here are illustrative, not statistically strong — the point of
> this project is the dataset-building and labeling process, documented
> honestly, not a production-grade classifier. See below for what that
> means concretely.

## Problem

When a company executive is asked a direct question on an earnings call,
how directly do they actually answer it? This project fine-tunes a small
LLM to classify analyst Q&A exchanges from real earnings calls as
**Direct**, **Partial**, or **Evasive**.

## Dataset

No existing dataset for this task, by nature of the question being
asked. Built from 8 public earnings call transcripts (fool.com), Q&A
sections only, 104 analyst-question / executive-answer exchanges.

**Labeling rubric:** written before any labeling began — see
[`docs/labeling-rubric.md`](docs/labeling-rubric.md).

**Labeling methodology:** AI-assisted first pass, human-reviewed. Claude
proposed a label and one-sentence reasoning for every exchange by
applying the rubric's decision procedure (`ai_proposed_label` /
`ai_reasoning` columns in the worksheet); the final label in the `label`
column is a human confirmation or correction of each one, not a
rubber stamp. This is disclosed as the actual methodology rather than
framed as pure manual labeling — see `docs/build-log.md` for why this
approach was chosen over labeling from blank.

**Inter-rater agreement:** a second rater independently labeled a
20-30 example sample using the same rubric. Agreement rate reported in
[`docs/README.md`](docs/README.md) once labeling is complete.

## Approach

Same small model + QLoRA method as the ticket triage project, reusing the
same Azure ML compute cluster and pipeline pattern. No polished deployed
endpoint for this one — the labeling process and honest writeup are the
deliverable, not a shipped product.

## Status

Just started. See [`docs/build-log.md`](docs/build-log.md) for progress.

## Reproduce

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
