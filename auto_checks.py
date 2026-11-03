"""
Objective, rule-based measurements of every answer (no LLM, no human judgement).

These are fully reproducible quantitative measures that complement the rubric scores:
  - format compliance: did the model follow the formatting instruction (F1, F2)?
  - citations: how many [n] citations, are they valid chunk numbers (1..k)?
  - refusals: did the model say the answer cannot be found?
      * for unanswerable questions a refusal is CORRECT
      * for answerable questions a refusal is a FALSE refusal

Run:  python auto_checks.py --set final
Output: results/<set>/auto_checks.csv
"""
import argparse
import re

import pandas as pd

import config
from experiment_io import results_dir

LIST_LINE = re.compile(r"^\s*([-*•]|\d+[.)])\s+", re.M)
NUMBERED_LINE = re.compile(r"^\s*\d+[.)]\s+", re.M)
HEADING_LINE = re.compile(r"^\s*(#{1,6}\s|\*\*[^*]+\*\*\s*:?\s*$)", re.M)
CITATION = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9`\"'(])")
REFUSAL_CORE = "cannot be found in the provided documentation"
# Broader: the answer says in its own words that the information is missing from the excerpts.
MISSING_INFO = re.compile(
    r"cannot be found|(?:not|no)\s+(?:explicitly\s+)?(?:mention|include|contain|cover|provide|describe|document|specif)"
    r"|does not (?:mention|include|contain|cover|provide|describe|specify)|isn.t (?:mentioned|covered|included)",
    re.I)


def count_sentences(text):
    text = CITATION.sub("", re.sub(r"```.*?```", " CODE. ", text, flags=re.S))
    return len([s for s in SENTENCE_END.split(text.strip()) if s.strip()])


def check(answer, formatting, k):
    answer = str(answer)
    numbers = [int(n) for group in CITATION.findall(answer) for n in group.split(",")]
    has_list = bool(LIST_LINE.search(answer))
    has_heading = bool(HEADING_LINE.search(answer))
    sentences = count_sentences(answer)
    if formatting == "F1":
        format_ok = (not has_list) and (not has_heading) and 3 <= sentences <= 5
    elif formatting == "F2":
        format_ok = len(NUMBERED_LINE.findall(answer)) >= 2
    else:
        format_ok = None  # baseline has no instruction to follow
    return {
        "n_chars": len(answer),
        "n_sentences": sentences,
        "has_list": has_list,
        "has_heading": has_heading,
        "format_compliant": format_ok,
        "n_citations": len(numbers),
        "has_citation": len(numbers) > 0,
        "citations_valid": all(1 <= n <= k for n in numbers) if numbers else None,
        "is_refusal": REFUSAL_CORE in answer.lower(),
        "acknowledges_missing": bool(MISSING_INFO.search(answer)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", default="final", choices=["pilot", "final"])
    args = parser.parse_args()
    out_dir = results_dir(args.set)
    answers = pd.read_csv(out_dir / "answers.csv")
    rows = [{"answer_id": a["answer_id"], **check(a["answer"], a["formatting"], config.TOP_K)}
            for _, a in answers.iterrows()]
    keep = [c for c in ["answer_id", "question_id", "llm", "type", "answerable", "formatting", "grounding"]
            if c in answers.columns]
    df = answers[keep].merge(
        pd.DataFrame(rows), on="answer_id")
    df["correct_refusal"] = df["is_refusal"].where(~df["answerable"])
    df["false_refusal"] = df["is_refusal"].where(df["answerable"])
    df["unanswerable_acknowledged"] = df["acknowledges_missing"].where(~df["answerable"])
    df.to_csv(out_dir / "auto_checks.csv", index=False)

    print("Format compliance by formatting strategy (%):")
    print((df.groupby("formatting")["format_compliant"].apply(lambda s: s.dropna().mean()) * 100).round(1))
    print("\nAnswers with at least one citation, by grounding strategy (%):")
    print((df.groupby("grounding")["has_citation"].mean() * 100).round(1))
    print("\nCorrect refusals on UNANSWERABLE questions, by grounding strategy (%):")
    print((df.groupby("grounding")["correct_refusal"].apply(lambda s: s.dropna().mean()) * 100).round(1))
    print("\nUNANSWERABLE questions where the answer admits the information is missing (own words), by grounding (%):")
    print((df.groupby("grounding")["unanswerable_acknowledged"].apply(lambda s: s.dropna().mean()) * 100).round(1))
    print("\nFalse refusals on ANSWERABLE questions, by grounding strategy (%):")
    print((df.groupby("grounding")["false_refusal"].apply(lambda s: s.dropna().mean()) * 100).round(1))


if __name__ == "__main__":
    main()
