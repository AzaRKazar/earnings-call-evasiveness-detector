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

**Inter-rater agreement:** a second rater independently labeled a blind
25-example sample using the same rubric, with no visibility into the
primary labels. Result: 68.0% raw agreement, **Cohen's kappa 0.375**
("fair," not "strong" — reported honestly rather than leading with the
friendlier raw number). All disagreements were adjacent-category, and
7 of 8 clustered specifically at the Direct/Partial boundary — a real,
specific finding about where the rubric under-specifies the task, not
just "labeling is subjective." Full writeup: [`docs/README.md`](docs/README.md).

## Approach

Same small model + QLoRA method as the ticket triage project, reusing the
same Azure ML compute cluster and pipeline pattern. No polished deployed
endpoint for this one — the labeling process and honest writeup are the
deliverable, not a shipped product.

## Status

Data gathered and verified, rubric written, all 104 exchanges labeled
(AI-assisted, human-reviewed), second-rater agreement computed. Next:
train/test split and QLoRA fine-tuning, gated on the same Azure GPU
quota blocker as the ticket triage project. See
[`docs/build-log.md`](docs/build-log.md) for the full progression.

## Reproduce

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
