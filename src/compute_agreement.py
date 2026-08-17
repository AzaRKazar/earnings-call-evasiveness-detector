"""Merge the second rater's blind labels into the main worksheet and
compute inter-rater agreement (raw percent + Cohen's kappa) against the
primary labeler, on the sampled subset only.
"""

import csv
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAIN_PATH = ROOT / "data" / "labeling_worksheet.csv"
RATER2_PATH = ROOT / "data" / "rater2_blind_sample_completed.csv"

LABELS = ["Direct", "Partial", "Evasive"]


def cohens_kappa(pairs: list[tuple[str, str]]) -> float:
    n = len(pairs)
    po = sum(1 for a, b in pairs if a == b) / n

    a_counts = Counter(a for a, _ in pairs)
    b_counts = Counter(b for _, b in pairs)
    pe = sum((a_counts[l] / n) * (b_counts[l] / n) for l in LABELS)

    if pe == 1.0:
        return 1.0
    return (po - pe) / (1 - pe)


def main() -> None:
    with open(MAIN_PATH, encoding="utf-8-sig") as f:
        main_rows = {r["id"]: r for r in csv.DictReader(f)}

    with open(RATER2_PATH, encoding="utf-8-sig") as f:
        rater2_rows = list(csv.DictReader(f))

    print(f"Second rater completed {len(rater2_rows)} rows")

    # Merge rater2_label back into the main worksheet
    for r2 in rater2_rows:
        row_id = r2["id"]
        if row_id in main_rows:
            main_rows[row_id]["rater2_label"] = r2["rater2_label"]
            if r2.get("notes"):
                main_rows[row_id]["notes"] = (
                    main_rows[row_id].get("notes", "") + f" [rater2: {r2['notes']}]"
                ).strip()

    fieldnames = [
        "id", "company", "ticker", "analyst", "executive", "question", "answer",
        "ai_proposed_label", "ai_reasoning", "label", "rater2_label", "notes",
    ]
    with open(MAIN_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row_id in sorted(main_rows, key=int):
            writer.writerow(main_rows[row_id])

    # Compute agreement on exactly the sampled subset
    pairs = []
    disagreements = []
    for r2 in rater2_rows:
        row_id = r2["id"]
        primary = main_rows[row_id]["label"].strip()
        secondary = r2["rater2_label"].strip()
        pairs.append((primary, secondary))
        if primary != secondary:
            disagreements.append((row_id, primary, secondary, main_rows[row_id]["company"]))

    n = len(pairs)
    agree = sum(1 for a, b in pairs if a == b)
    pct = agree / n * 100
    kappa = cohens_kappa(pairs)

    print(f"\nSample size: {n}")
    print(f"Raw agreement: {agree}/{n} ({pct:.1f}%)")
    print(f"Cohen's kappa: {kappa:.3f}")
    print(f"\nPrimary label distribution on this subset: {dict(Counter(a for a, _ in pairs))}")
    print(f"Rater2 label distribution on this subset:  {dict(Counter(b for _, b in pairs))}")

    print(f"\nDisagreements ({len(disagreements)}):")
    for row_id, primary, secondary, company in disagreements:
        print(f"  ID {row_id} ({company}): primary='{primary}' vs rater2='{secondary}'")


if __name__ == "__main__":
    main()
