"""Merge Claude's first-pass labels + reasoning into the labeling worksheet.

Written as a script rather than edited into the CSV by hand, for the same
reason build_worksheet.py was: deterministic and re-runnable beats manual
editing of a 104-row file, given how many manual transcription slips this
project has already caught and fixed.
"""

import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "labeling_worksheet.csv"

# id -> (label, reasoning)
AI_LABELS: dict[int, tuple[str, str]] = {
    1: ("Direct", "Confirms the ~3% growth assumption is roughly right and adds real color (extra day, loan/securities growth) on 'anything else to consider.'"),
    2: ("Direct", "Gives the specific mechanism for stabilization (market balance sheet growth moderating) and a concrete near-term path (small Q3 decline, then stabilize)."),
    3: ("Direct", "Question was open-ended/directional, not asking for a hard number; answer substantively confirms continued headcount efficiency with real drivers (tech/AI)."),
    4: ("Direct", "Explicitly rules out checking-account growth as the cause and gives the rate-environment explanation as the alternative -- directly answers the either/or framing."),
    5: ("Partial", "Gives real numbers on deposit costs, but doesn't engage the specific structural-vs-cyclical framing or the markets-dilutive-vs-card-accretive dynamic the analyst explicitly asked to separate."),
    6: ("Partial", "IB pipeline gets decent color; the specific prime financing opportunity (the actual ask) gets 'nothing material' without engaging the competitor-capacity premise at all."),
    7: ("Direct", "Directly confirms NIM stabilization and gives numbers-backed detail (financing revenue ~2x, trading revenue +20%+) on the cross-sell question."),
    8: ("Evasive", "Explicitly declines to give any timing color ('not giving a definitive time frame') on a question that was entirely about timing -- the one thing asked for is the one thing withheld."),
    9: ("Direct", "Directly answers the utilization-vs-new-business question with a clear stance (new business) and confirms auto growth continuing."),
    10: ("Partial", "Confirms the target range but doesn't explain the quarter's dip below the recent base or give real forward specificity beyond 'we'll decide quarter to quarter.'"),
    11: ("Direct", "Direct yes to a yes/no-shaped clarifying question, with a soft timing hint."),
    12: ("Partial", "Real qualitative color on acquisition cost/quality, but no quantified 'drag' estimate and no specific inflection timing despite both being explicitly requested."),
    13: ("Direct", "Directly answers both parts: confirms growth confidence ('yes') and states pricing competition hasn't changed from expectations."),
    14: ("Partial", "Confirms directionally that this is an efficiency lever but stays generic ('methodical,' 'over time') with no real magnitude or timeline despite an open invitation to elaborate."),
    15: ("Direct", "Thorough, specific engagement with both consumer and commercial health questions -- delinquency trends, cohort analysis, no-firing-but-cautious commercial color."),
    16: ("Direct", "Directly corrects the premise (not comfort-level driven) and explains the actual mechanism (post-asset-cap reemergence); part 2 gets reasonable directional confirmation."),
    17: ("Direct", "Specific, substantive claims (record recruiting, record-low attrition) directly responsive to competitiveness and pipeline."),
    18: ("Direct", "Directly refutes the premise of a 'shift' with cited specifics (consistent language since January, at conferences) rather than dodging the question."),
    19: ("Direct", "Cites specific factors (seasonality, tariff refund paydowns) and explicitly rules out a sentiment change; gives forward view by segment."),
    20: ("Direct", "Nuanced, substantive answer distinguishing consumer (no risk-taking seen) from wholesale (real color on where/how) as asked."),
    21: ("Partial", "Engages the direct-measurement question reasonably but the 'second derivative effect on better quality customers' part stays vague."),
    22: ("Direct", "Detailed, specific discussion of different financing types and risk/payback profiles -- genuinely engages the nuanced ask."),
    23: ("Partial", "No number given despite an explicit 'quantify in numbers' ask, but the qualitative reasoning (macro dependency, investment plan) is real, not a non-answer."),
    24: ("Evasive", "Explicit upfront refusal of the requested precision ('may disappoint you in not giving precise math'), followed by a generic framework rather than confirming/denying the specific range floated."),
    25: ("Partial", "Denies the 'much worse 2H' premise (somewhat responsive) but never engages the specific math the analyst laid out, nor names which areas would see accelerated spending."),
    26: ("Partial", "Explicit refusal on the specific percentage asked for, but the sequencing question (wait for 100% vs. rolling handover) gets real, if indirect, substance."),
    27: ("Direct", "Explains why guidance wasn't raised (expects 19% deposit growth to normalize) -- a real answer to 'why not better,' not just reassurance."),
    28: ("Partial", "Specific YTD severance numbers given (Direct); 2H magnitude explicitly declined ('not providing a specific number now')."),
    29: ("Partial", "Broad reassurance across business lines without directly engaging the 'worse vs. replicate' or 'step shift' framing the analyst set up."),
    30: ("Direct", "Specific numbers throughout (return targets, 22% actual return, 82%->84% card mix) directly addressing the revenue-vs-expense trajectory asked."),
    31: ("Direct", "Comprehensive, numbers-backed walk-through of exactly the capital-path factors asked about (Basel III/GSIB, SCB trajectory with real bps figures)."),
    32: ("Direct", "Specific DTA numbers ($13.9B->$13.4B, $500M of $800M consumed) and named drivers given."),
    33: ("Evasive", "Explicitly says 'there is nothing specifically' then gives a generic hand-wave despite a direct ask for specifics; doesn't address the return-timing part at all."),
    34: ("Partial", "Describes a favorable macro/deal environment with one example, but stays at 'the environment is good' level rather than detailing Citi's own specific pipeline as asked."),
    35: ("Direct", "Clear, direct 'not looking at changing the buffer right now' with supporting reasoning."),
    36: ("Direct", "Specific, thorough engagement -- spend growth figures, delinquency/loss trends down YoY, explicit watch-items named."),
    37: ("Partial", "Consent-order expense timing answered directly; the 'better half of the target range' framing is explicitly deflected ('do not read anything more into it')."),
    38: ("Direct", "Substantive, segment-by-segment engagement (services vs. wealth) on deposit cost trajectory as asked."),
    39: ("Direct", "Explains both the elevated current level (drivers) and the normalization expectation (historical baseline cited) with real context."),
    40: ("Direct", "Genuinely engages the actual question with balanced reasoning on both scenarios (better or worse than the historical 20%) rather than hiding behind vague reassurance."),
    41: ("Direct", "Specific regional breakdown (Europe/US/China/Asia) genuinely addressing 'how' as asked, not just 'that.'"),
    42: ("Direct", "Clear 'in a word, no' followed by real explanation and contrast."),
    43: ("Direct", "Gives a real timeline (early 2027 deconsolidation, IPO to follow) and reasoning for the pacing."),
    44: ("Direct", "Specific estimate given ($5B capital, ~$40B RWA) exactly as requested."),
    45: ("Partial", "Confirms marketing spend WILL increase (direct) but explicitly declines to size the incremental investment/headwind as asked."),
    46: ("Partial", "Real driver color and numbers on the margin story, but the explicit 'any color on recent wins' ask gets no concrete examples."),
    47: ("Partial", "Explicitly refuses the requested geographic breakdown; substitutes real but different metrics (market share, client wins) instead."),
    48: ("Direct", "Enumerates specific priorities (Kokai/Zuma, measurement/Audience Unlimited, JBPs, leadership) with supporting data, matching what was asked."),
    49: ("Partial", "States a real philosophy (invest with conviction, discipline elsewhere) but stays generic and explicitly defers specifics ('stay tuned')."),
    50: ("Partial", "Publicis relationship answered directly; the explicit 'quantify both' (control vs. macro) ask gets qualitative color only, never quantified."),
    51: ("Direct", "Detailed two-bucket framework with specific supporting stats (60% more traveler intent info, 2/3 direct bookings)."),
    52: ("Partial", "Andersen's efficiency answer is specific (overhead flat YoY vs. 14% revenue growth); Gorin's stickiness/advantages answer stays generic."),
    53: ("Partial", "Andersen's margin answer is specific (named factors, ~50bps Q4 implied); Gorin's geo answer is generic and doesn't address 'how have views changed.'"),
    54: ("Partial", "Andersen names the two specific overhead drivers (Tiqets, FX hedging geography); Gorin's competitive-landscape answer stays at market-sizing generality."),
    55: ("Direct", "Both parts get real, specific engagement -- organic traffic detail with a named initiative, and specific Middle East/comp-driven booking guidance."),
    56: ("Partial", "AEO gets genuine color but doesn't resolve the specific 'bigger in the US or unique approach' framing; the 'what surprised you' question gets a generic non-answer."),
    57: ("Partial", "Drivers are very specific (8% bookings vs. 1% marketing spend, named levers); the explicit 'runway into 2027' ask gets zero engagement."),
    58: ("Partial", "World Cup impact answered specifically (modest, more in ADRs); advertising 'traction' answered only vaguely ('stable... a lot of opportunity')."),
    59: ("Partial", "Borderline case -- makes a clear claim ('normalized') but gives zero elaboration despite the question explicitly asking for 'more color.' See rubric Worked Example 6."),
    60: ("Direct", "Real drivers named (partner promotional activity, investment pacing, partner-base growth) directly addressing what was asked."),
    61: ("Partial", "Legitimate non-disclosure on the Uber partnership (explicit, reasoned), combined with a genuinely detailed answer on attach rates. See rubric Worked Example 4."),
    62: ("Partial", "Confirms real runway exists but explicitly declines to quantify ('without going into what exactly those numbers are') and doesn't engage the specific 'inning' framing."),
    63: ("Partial", "General capital-strength reassurance without ever identifying or denying a structural constraint, which was the actual question."),
    64: ("Direct", "Directly answers 'is it moderating' (no) with specific supporting examples (named state reforms)."),
    65: ("Partial", "The specific years asked about (2021, 2022) are never addressed at all -- only 2023 and 2016 are discussed, despite real substance on the broader reserving process."),
    66: ("Direct", "Specific, real mechanism explained (Q2 seasonality, casualty mix shift, offsetting personal-insurance strength) directly addressing the loss-ratio question."),
    67: ("Partial", "Growth/M&A appetite addressed with real numbers, but the specific 'will pricing get more competitive' forecast is never directly answered."),
    68: ("Partial", "Real color on growth drivers across segments, but 'how big a factor' premium growth is to the ROE math is never actually quantified."),
    69: ("Partial", "Substantial qualitative color on the AI initiative, but the direct 'noticeable difference yet, or still WIP' binary is never crisply resolved."),
    70: ("Evasive", "Explicit 'we haven't really broken out the pieces' refusal on the specific ask (size the Convex contribution); no substitute number for Convex itself is given."),
    71: ("Direct", "Specific, quantified, unhedged answer (16bps) to a yes/no-shaped question. See rubric Worked Example 2."),
    72: ("Direct", "Despite an opening hedge, gives real quantified drivers (7% NPW growth, 220bps expense improvement, 490bps combined ratio improvement) and named causes."),
    73: ("Direct", "Specific numbers on both parts -- expense ratio trend (30.7% vs. 31.1%) and a clear framing of AI's role (efficiency/redeployment, not headcount cuts)."),
    74: ("Partial", "General reassurance without directly answering the specific 'low end or below' positioning question asked."),
    75: ("Direct", "Real number given (17.6%, within range) plus a clear implicit 'no plans to change' position."),
    76: ("Direct", "Lists specific, enumerated drivers (technology, evidence, UX, team) with real supporting numbers (34K vs. prior 25K record)."),
    77: ("Partial", "Explicit refusal on exact timing/full specificity ('cannot provide details on every single study'), though one study is named and ER101 gets deep engagement."),
    78: ("N/A", "Not a real question -- 'Great, thanks, guys' is a closing acknowledgment, not an ask. Recommend excluding from the final labeled set rather than forcing a label."),
    79: ("Direct", "Real specific numbers (34K vs. 25K prior record) and clear reasoning for why the pace won't repeat immediately, plus directional confidence."),
    80: ("Direct", "Specific numeric answer (stable $12.75 base case, ~$25 upside case) directly matching the specific numeric question asked."),
    81: ("Partial", "Real market-share color (mid-single-digit penetration) given, but the specific 'lanes for each / crossover' competitive-dynamics framing isn't directly addressed."),
    82: ("Partial", "Real context on submission status and segment growth, but stays deliberately non-specific on the mix itself, as both analyst and executive seem to expect."),
    83: ("Direct", "Gives a real timeline and a specific dollar estimate ($150-200 ASP) that directly confirms the analyst's own ballpark."),
    84: ("Direct", "Clear, direct answer: no big retrospective bolus expected, ongoing gradual process instead -- directly answers the yes/no-shaped ask."),
    85: ("Direct", "Direct 'yes' on share gains with specific supporting evidence (named product launches, competitive positioning)."),
    86: ("Partial", "Specific attribution for the SG&A delta (named one-time items); the AI-savings progress against the analyst's own $200M reference gets no real update."),
    87: ("Partial", "Good structural color on coverage sequencing and market positioning, but the literal 'how quickly could reps get out there' timing isn't quantified."),
    88: ("Direct", "Clear mechanism explained (scale efficiencies then deliberate workflow investment) with explicit timing (12-18 months)."),
    89: ("Partial", "ECD timeline and margin cause both confirmed directly; the specific 'flip later this year' timing question isn't crisply confirmed or denied."),
    90: ("Direct", "Directly answers the either/or framing ('a bit of both') with specific supporting detail (completion percentages, demand signal)."),
    91: ("Direct", "Explains the two-part structure clearly with a real specific outcome (accelerated to end of 2027 vs. 2028)."),
    92: ("Evasive", "Explicitly declines to give the specific magnitude estimate asked for ('not ready to unpack... we'll give you a peek'), deferring entirely to a future forecast."),
    93: ("Direct", "Specific numbers for both current state (~9.5-9.8 scheduled lines) and potential upside (10-15%) given by the two executives."),
    94: ("Direct", "Direct, specific ownership percentage given exactly as asked."),
    95: ("Direct", "Comprehensive, numbers-heavy answer covering both growth metrics and the specific NII guidance concern with real hedge/FX caveats."),
    96: ("Direct", "Specific breakdown of where savings came from and real directional numbers on cost growth trend, even without a single crisp future percentage."),
    97: ("Evasive", "Explicit refusal to comment on the specific consensus number asked about, and the payback timeframe question is never actually answered."),
    98: ("Partial", "Most sub-questions (hedging, HIBOR, deposits, cross-border rules) get thorough specific answers, but the flagged 'AUM outside Asia declined' data point is never addressed."),
    99: ("Partial", "Some genuine color on payoff speed (quick, not 1-2 years), but the specific magnitude-vs-$500M comparison the analyst asked for is never addressed."),
    100: ("Evasive", "Explicit non-answer to a narrow, answerable timing question, replaced with generic strategic reassurance. See rubric Worked Example 5."),
    101: ("Direct", "Extremely specific throughout -- loan/capital-markets detail with real percentages, and precise Hang Seng synergy numbers ($500M+$400M, 80% execution, named onboarding figures)."),
    102: ("Partial", "Asset quality and Middle East reserve answers are very specific and numbers-heavy; the 'are regulators consulting industry players' question gets a generic non-answer."),
    103: ("Partial", "Strategic-direction question gets a thorough, specific answer with a named example (Egypt); the 'where would you use shares as currency' question gets criteria but no actual candidate areas."),
    104: ("Direct", "Directly engages 'broad-based or concentrated' with real segment-level detail and specific growth figures (CIB +16% YoY, named sectors)."),
}


def main() -> None:
    with open(CSV_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    if "ai_proposed_label" not in fieldnames:
        # Insert new columns right after 'answer', before the human label column
        idx = fieldnames.index("answer") + 1
        fieldnames = fieldnames[:idx] + ["ai_proposed_label", "ai_reasoning"] + fieldnames[idx:]

    missing = []
    for row in rows:
        row_id = int(row["id"])
        if row_id in AI_LABELS:
            label, reasoning = AI_LABELS[row_id]
            row["ai_proposed_label"] = label
            row["ai_reasoning"] = reasoning
        else:
            missing.append(row_id)

    if missing:
        print(f"WARNING: no AI label for ids: {missing}")

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    from collections import Counter
    dist = Counter(AI_LABELS[int(r["id"])][0] for r in rows if int(r["id"]) in AI_LABELS)
    print(f"Applied {len(AI_LABELS)} labels. Distribution: {dict(dist)}")
    print(f"Wrote {CSV_PATH}")


if __name__ == "__main__":
    main()
