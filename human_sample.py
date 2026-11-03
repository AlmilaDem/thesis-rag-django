"""
Creates a BLIND scoring form for the external reviewer (thesis Section 2.4, hybrid scoring).

A stratified random sample (HUMAN_SAMPLE_SHARE of the judged answers, spread over all
9 strategy combinations) is exported to Excel. The reviewer does not see the strategy
codes or the automatic scores. The key that links sample numbers to answers is saved
separately.

Run:  python human_sample.py --set final
Output: results/<set>/human_scoring_form.xlsx   (send this to the reviewer)
        results/<set>/human_key.csv             (keep this, do NOT send)
"""
import argparse

import pandas as pd

import config
from experiment_io import load_questions, load_retrieved, results_dir


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", default="final", choices=["pilot", "final"])
    args = parser.parse_args()
    out_dir = results_dir(args.set)
    questions = load_questions(args.set).set_index("id")
    retrieved = load_retrieved(args.set)
    answers = pd.read_csv(out_dir / "answers.csv")
    answers = answers[answers["answerable"]]

    strata = [c for c in ["llm", "formatting", "grounding"] if c in answers.columns]
    n_groups = answers.groupby(strata).ngroups
    per_combo = max(1, round(len(answers) * config.HUMAN_SAMPLE_SHARE / n_groups))
    parts = [group.sample(min(per_combo, len(group)), random_state=config.SEED)
             for _, group in answers.groupby(strata)]
    sample = (pd.concat(parts)
              .sample(frac=1, random_state=config.SEED)   # shuffle so strategies are mixed
              .reset_index(drop=True))
    sample["sample_no"] = range(1, len(sample) + 1)

    form = pd.DataFrame({
        "sample_no": sample["sample_no"],
        "question_type": sample["question_id"].map(questions["type"]),
        "question": sample["question"],
        "reference_answer": sample["question_id"].map(questions["reference_answer"]),
        "retrieved_documentation": sample["question_id"].map(
            lambda qid: "\n\n".join(f"[{n}] {c['text']}" for n, c in enumerate(retrieved[qid], 1))),
        "answer": sample["answer"],
    })
    for criterion in config.CRITERIA:
        form[criterion] = ""
    form["comment"] = ""
    with pd.ExcelWriter(out_dir / "human_scoring_form.xlsx") as writer:
        form.to_excel(writer, sheet_name="scoring", index=False)
        pd.DataFrame({"Instructions": [
            "Score every answer from 1 to 5 on each criterion (5 = best). Use 2 and 4 for in-between answers.",
            "technical_correctness: compare with the reference answer. 5 fully correct, 3 partly correct, 1 incorrect.",
            "clarity: 5 clear and well structured, 3 understandable but hard to follow in places, 1 confusing.",
            "faithfulness: compare with the retrieved documentation. 5 all main claims supported, 3 some not supported, 1 most not supported.",
            "hallucination_control: 5 no unsupported claims, 3 one or two unsupported details, 1 many unsupported claims.",
            "answer_relevance: 5 fully answers the question, 3 partly, 1 does not answer.",
        ]}).to_excel(writer, sheet_name="instructions", index=False)
    sample[["sample_no", "answer_id"] + strata].to_csv(out_dir / "human_key.csv", index=False)
    print(f"{len(sample)} answers exported to human_scoring_form.xlsx ({per_combo} per strategy combination).")


if __name__ == "__main__":
    main()
