"""
Retrieval verification (thesis Sections 2.4 and 5.2) and choice of k during the pilot.

For each answerable question it checks whether the expected source is among the first k
retrieved chunks, for several values of k. Cheap: only embeddings are used, no LLM.

Run:  python check_retrieval.py --set pilot
Output: results/<set>/retrieval_by_k.csv
"""
import argparse

import pandas as pd

from experiment_io import load_questions, results_dir, source_hit
from rag import retrieve

K_VALUES = [1, 3, 5, 7, 10]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", default="pilot", choices=["pilot", "final"])
    args = parser.parse_args()
    questions = load_questions(args.set)
    questions = questions[questions["answerable"]]
    rows = []
    for _, q in questions.iterrows():
        found = retrieve(q["question"], max(K_VALUES))
        for k in K_VALUES:
            page_hit, section_hit = source_hit(found[:k], q["expected_page"], q["expected_section"])
            rows.append({"id": q["id"], "type": q["type"], "k": k,
                         "page_hit": page_hit, "section_hit": section_hit})
    df = pd.DataFrame(rows)
    df.to_csv(results_dir(args.set) / "retrieval_by_k.csv", index=False)
    summary = df.groupby("k").agg(page_hit_rate=("page_hit", "mean"),
                                  section_hit_rate=("section_hit", lambda s: s.dropna().mean()))
    print((summary * 100).round(1).astype(str) + " %")
    print("\nChoose the smallest k with a high hit rate, write it into config.TOP_K, and freeze it.")


if __name__ == "__main__":
    main()
