# Earnings Call Evasiveness Detector

> **Exploratory project.** This is a small, self-labeled dataset (~120-150
> examples) built and labeled from scratch, fine-tuned with the same QLoRA
> approach as the [ticket triage project](https://github.com/AzaRKazar/support-ticket-triage-llm-finetuning).
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

Self-labeled. No existing dataset for this task, by nature of the
question being asked. Built from 5-8 public earnings call transcripts
(Motley Fool / Seeking Alpha), Q&A sections only, ~120-150
analyst-question / executive-answer exchanges.

**Labeling rubric:** written before any labeling began — see
[`docs/labeling-rubric.md`](docs/labeling-rubric.md).

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
