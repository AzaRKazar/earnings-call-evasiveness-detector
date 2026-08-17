"""Parse the raw transcript markdown files into a single labeling worksheet.

Written as a script rather than hand-copied into a spreadsheet on
purpose: manual transcription already caused two real data errors in
this project (a truncated answer, an undercounted exchange list), and a
deterministic, re-runnable parser is the fix for that class of mistake.
"""

import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw_transcripts"
OUT_PATH = ROOT / "data" / "labeling_worksheet.csv"

COMPANIES = {
    "wells_fargo_q2_2026.md": ("Wells Fargo", "WFC"),
    "citi_q2_2026.md": ("Citi", "C"),
    "trade_desk_q2_2026.md": ("Trade Desk", "TTD"),
    "expedia_q2_2026.md": ("Expedia", "EXPE"),
    "aig_q2_2026.md": ("AIG", "AIG"),
    "natera_q2_2026.md": ("Natera", "NTRA"),
    "republic_airways_q2_2026.md": ("Republic Airways", "RJET"),
    "hsbc_q2_2026.md": ("HSBC", "HSBC"),
}

EXCHANGE_RE = re.compile(
    r"^## Exchange \d+\s*\n"
    r"\*\*Analyst:\*\* (?P<analyst>.+?)\s*\n"
    r"\*\*Executive:\*\* (?P<executive>.+?)\s*\n\n"
    r"\*\*Question:\*\*\s*(?P<question>.+?)\n\n"
    r"(?:\*\*Answer[^:]*:\*\*\s*(?P<answer>.+?))(?=\n## Exchange|\Z)",
    re.DOTALL | re.MULTILINE,
)

CONTINUATION_RE = re.compile(r"^\(Continuation of Exchange", re.IGNORECASE)


def parse_file(path: pathlib.Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    exchanges = []
    for m in EXCHANGE_RE.finditer(text):
        exchanges.append(
            {
                "analyst": m.group("analyst").strip(),
                "executive": m.group("executive").strip(),
                "question": m.group("question").strip().strip('"'),
                "answer": (m.group("answer") or "").strip().strip('"'),
            }
        )
    return exchanges


def merge_continuations(exchanges: list[dict]) -> list[dict]:
    merged: list[dict] = []
    for ex in exchanges:
        if CONTINUATION_RE.match(ex["question"]) and merged:
            prev = merged[-1]
            prev["answer"] += "\n\n[continued by " + ex["executive"] + "]\n\n" + ex["answer"]
            prev["executive"] += " / " + ex["executive"]
        else:
            merged.append(ex)
    return merged


def main() -> None:
    rows = []
    exchange_id = 1
    for filename, (company, ticker) in COMPANIES.items():
        path = RAW_DIR / filename
        if not path.exists():
            print(f"WARNING: missing {filename}")
            continue
        exchanges = parse_file(path)
        exchanges = merge_continuations(exchanges)
        print(f"{filename}: {len(exchanges)} exchanges after merging continuations")
        for ex in exchanges:
            rows.append(
                {
                    "id": exchange_id,
                    "company": company,
                    "ticker": ticker,
                    "analyst": ex["analyst"],
                    "executive": ex["executive"],
                    "question": ex["question"],
                    "answer": ex["answer"],
                    "label": "",
                    "rater2_label": "",
                    "notes": "",
                }
            )
            exchange_id += 1

    print(f"\nTotal exchanges: {len(rows)}")

    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id", "company", "ticker", "analyst", "executive",
                "question", "answer", "label", "rater2_label", "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
