"""
STEP 4+5 - Runs the experiment (thesis Section 2.5, steps 4 and 5).

1) Retrieval is done ONCE per question and saved (retrieved.json). If the file already
   exists it is reused, so all strategies get exactly the same context.
2) For every question x every LLM x every formatting strategy x every grounding strategy
   (2 x 3 x 3 = 18 combinations) one answer is generated and saved.

The script can be stopped and started again: answers that already exist are skipped.

Run:  python run_experiment.py --set pilot
      python run_experiment.py --set final
Output: results/<set>/retrieved.json, retrieval_check.csv, prompts.jsonl, answers.csv
"""
import argparse
import json
from datetime import datetime

import pandas as pd

import config
from experiment_io import load_questions, results_dir, source_hit
from rag import generate, retrieve


def do_retrieval(questions, out_dir, k):
    path = out_dir / "retrieved.json"
    if path.exists():
        print("Using saved retrieval results (retrieved.json).")
        return json.loads(path.read_text(encoding="utf-8"))
    print(f"Retrieving top-{k} chunks for {len(questions)} questions ...")
    retrieved = {q["id"]: retrieve(q["question"], k) for _, q in questions.iterrows()}
    path.write_text(json.dumps(retrieved, indent=2, ensure_ascii=False), encoding="utf-8")
    rows = []
    for _, q in questions.iterrows():
        page_hit, section_hit = source_hit(retrieved[q["id"]], q["expected_page"], q["expected_section"])
        rows.append({"id": q["id"], "type": q["type"], "answerable": q["answerable"],
                     "page_hit": page_hit if q["answerable"] else None,
                     "section_hit": section_hit if q["answerable"] else None,
                     "retrieved": " ; ".join(f"{c['page']}/{c['section']}" for c in retrieved[q["id"]])})
    check = pd.DataFrame(rows)
    check.to_csv(out_dir / "retrieval_check.csv", index=False)
    answerable = check[check["answerable"]]
    print(f"Expected page found in top-{k}: {answerable['page_hit'].mean() * 100:.1f} % of answerable questions")
    return retrieved


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", default="pilot", choices=["pilot", "final"])
    parser.add_argument("--limit", type=int, default=None, help="only the first N questions (for a quick try)")
    args = parser.parse_args()

    questions = load_questions(args.set)
    if args.limit:
        questions = questions.head(args.limit)
    out_dir = results_dir(args.set)
    retrieved = do_retrieval(questions, out_dir, config.TOP_K)

    answers_path = out_dir / "answers.csv"
    done = set(pd.read_csv(answers_path)["answer_id"]) if answers_path.exists() else set()
    combos = [(llm, f, g) for llm in config.GEN_MODELS for f in config.FORMATTING for g in config.GROUNDING]
    total = len(questions) * len(combos)
    print(f"Generating {total} answers ({len(done)} already done) with {list(config.GEN_MODELS.values())} ...")

    for _, q in questions.iterrows():
        for llm, f_code, g_code in combos:
            answer_id = f"{q['id']}_{llm}_{f_code}_{g_code}"
            if answer_id in done:
                continue
            answer, messages, meta = generate(q["question"], retrieved[q["id"]], f_code, g_code,
                                              config.GEN_MODELS[llm])
            row = {"answer_id": answer_id, "question_id": q["id"], "llm": llm, "type": q["type"],
                   "answerable": q["answerable"], "formatting": f_code, "grounding": g_code,
                   "question": q["question"], "answer": answer,
                   "model": meta["model"], "system_fingerprint": meta["system_fingerprint"],
                   "prompt_tokens": meta["prompt_tokens"], "completion_tokens": meta["completion_tokens"],
                   "generated_at": datetime.now().isoformat(timespec="seconds")}
            pd.DataFrame([row]).to_csv(answers_path, mode="a", index=False,
                                       header=not answers_path.exists())
            with open(out_dir / "prompts.jsonl", "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"answer_id": answer_id, "messages": messages}, ensure_ascii=False) + "\n")
            done.add(answer_id)
            print(f"  [{len(done)}/{total}] {answer_id}")
    print(f"Finished. Answers are in {answers_path}")


if __name__ == "__main__":
    main()
