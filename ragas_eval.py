"""
STEP 6 - Scoring with the RAGAS library (thesis Section 2.4, Table 2.4).

For every answer to an ANSWERABLE question, all five criteria are computed with RAGAS:

  criterion              RAGAS metric                       compared with       scale
  technical_correctness  Factual Correctness (F1)           reference answer    0-1
  clarity                Rubrics-based scoring (Table 2.3)  question            1-5
  faithfulness           Faithfulness                       retrieved context   0-1
  hallucination_control  Rubrics-based scoring (Table 2.3)  retrieved context   1-5
  answer_relevance       Response Relevancy                 question            0-1

The evaluator LLM is config.JUDGE_MODEL (Mistral API); the embeddings for Response Relevancy
are the same local model as the retrieval (config.EMBEDDING_MODEL).

Install once (inside the activated .venv):  pip install -r requirements-ragas.txt
Run:  python ragas_eval.py --set pilot
Works in small batches; it can be stopped and restarted (finished answers are skipped).
NaN policy: answers with an empty score are evaluated once more on the next run; after two
attempts an empty score is kept and excluded per criterion in analyze.py.
Output: results/<set>/ragas_scores.csv
"""
import argparse
import os
import re

import pandas as pd

import config
from experiment_io import load_questions, load_retrieved, results_dir

BATCH = 5
# Citation markers such as [1] are removed before the evaluation: otherwise the evaluator treats
# "[3]" as an unsupported claim and unfairly penalises the inline-citation strategy (G1).
# Whether the citations themselves are correct is measured separately in auto_checks.py.
CITATION = re.compile(r"\s*\[\d+(?:\s*,\s*\d+)*\]")

# Rubrics from Table 2.3 (scores 2 and 4 lie between the defined levels).
CLARITY_RUBRIC = {
    "score1_description": "The answer is confusing or poorly structured, or it does not address the question.",
    "score2_description": "The answer is hard to follow: important parts are unclear, or the structure clearly does not fit the question.",
    "score3_description": "The answer is understandable but hard to follow in places, e.g. it repeats itself, contains irrelevant or unnecessary detail, uses long wordy sentences, or its structure does not fit the type of question.",
    "score4_description": "The answer is clear overall but has minor issues, e.g. some unnecessary detail or repetition, or a length or structure that is slightly unsuitable for the question.",
    "score5_description": "The answer is clear, concise and well structured for the type of question that was asked: it contains no unnecessary content or repetition, and its structure suits the question (e.g. ordered steps for a procedure, a short direct answer for a definition).",
}
HALLUCINATION_RUBRIC = {
    "score1_description": "The answer contains many claims or details that are not supported by the retrieved context.",
    "score2_description": "The answer contains several (more than two) unsupported claims or details.",
    "score3_description": "The answer contains one or two claims or details that are not supported by the retrieved context.",
    "score4_description": "The answer contains one minor detail that is not clearly supported by the retrieved context.",
    "score5_description": "Every claim and detail in the answer is supported by the retrieved context (no unsupported claims).",
}
SCORE_COLUMNS = config.CRITERIA


def build_evaluators():
    from langchain_core.rate_limiters import InMemoryRateLimiter
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_mistralai import ChatMistralAI
    from ragas.embeddings import LangchainEmbeddingsWrapper
    from ragas.llms import LangchainLLMWrapper

    _, requests_per_second = config.RATE_LIMITS.get(config.JUDGE_MODEL, (20_000, 1.0))
    limiter = InMemoryRateLimiter(requests_per_second=requests_per_second * 0.8,
                                  check_every_n_seconds=0.1, max_bucket_size=1)
    chat = ChatMistralAI(model=config.JUDGE_MODEL, temperature=0, max_retries=10,
                         api_key=os.environ["MISTRAL_API_KEY"], rate_limiter=limiter)
    embeddings = HuggingFaceEmbeddings(model_name=f"sentence-transformers/{config.EMBEDDING_MODEL}")
    return LangchainLLMWrapper(chat), LangchainEmbeddingsWrapper(embeddings)


def pick(df, prefix):
    """RAGAS names some columns with suffixes, e.g. 'factual_correctness(mode=f1)'."""
    for column in df.columns:
        if column.startswith(prefix):
            return df[column].values
    raise KeyError(f"RAGAS result has no column starting with '{prefix}': {list(df.columns)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", default="final", choices=["pilot", "final", "variability"])
    parser.add_argument("--limit", type=int, default=None, help="evaluate at most N answers (quick test)")
    args = parser.parse_args()

    from ragas import EvaluationDataset, RunConfig, evaluate
    from ragas.metrics import Faithfulness, FactualCorrectness, ResponseRelevancy, RubricsScore

    if args.set == "variability":
        # repeated answers of variability.py (all to answerable final questions)
        out_dir = results_dir("final") / "variability"
        retrieved = load_retrieved("final")
        questions = load_questions("final").set_index("id")
        answers = pd.read_csv(out_dir / "variability_answers.csv").rename(columns={"run_id": "answer_id"})
        answers["question"] = answers["question_id"].map(questions["question"])
        answers["answerable"] = True
    else:
        out_dir = results_dir(args.set)
        retrieved = load_retrieved(args.set)
        questions = load_questions(args.set).set_index("id")
        answers = pd.read_csv(out_dir / "answers.csv")
    answers = answers[answers["answerable"]].reset_index(drop=True)

    out_path = out_dir / "ragas_scores.csv"
    done, attempts_before = set(), {}
    if out_path.exists():
        previous = pd.read_csv(out_path)
        if not set(SCORE_COLUMNS).issubset(previous.columns):   # file from an older version
            previous.to_csv(out_dir / "ragas_scores_old_version.csv", index=False)
            previous = previous.iloc[0:0]
        if "attempts" not in previous.columns:
            previous["attempts"] = 1
        # NaN policy: an answer with an empty score is evaluated ONE more time. If a score is
        # still empty after the second attempt it is kept as empty; analyze.py then leaves out
        # only that criterion for that answer and reports how many scores are missing.
        complete = previous[SCORE_COLUMNS].notna().all(axis=1)
        keep = previous[complete | (previous["attempts"] >= 2)]
        retry = previous[~complete & (previous["attempts"] < 2)]
        attempts_before = dict(zip(retry["answer_id"], retry["attempts"]))
        keep.to_csv(out_path, index=False)
        done = set(keep["answer_id"])
    todo = answers[~answers["answer_id"].isin(done)].reset_index(drop=True)
    if args.limit:
        # spread the quick test over all questions and conditions instead of the first rows
        todo = todo.sample(n=min(args.limit, len(todo)), random_state=42).reset_index(drop=True)
    print(f"RAGAS: {len(todo)} answers to evaluate ({len(done)} already done), evaluator {config.JUDGE_MODEL}")
    if todo.empty:
        return

    llm, embeddings = build_evaluators()
    with_reference = [FactualCorrectness(mode="f1"), Faithfulness(), ResponseRelevancy()]
    rubric_metrics = [RubricsScore(name="clarity", rubrics=CLARITY_RUBRIC),
                      RubricsScore(name="hallucination_control", rubrics=HALLUCINATION_RUBRIC)]
    run_config = RunConfig(max_workers=1, max_retries=10, max_wait=60, timeout=300)

    for start in range(0, len(todo), BATCH):
        batch = todo.iloc[start:start + BATCH]
        base = [{"user_input": a["question"],
                 "retrieved_contexts": [c["text"] for c in retrieved[a["question_id"]]],
                 "response": CITATION.sub("", str(a["answer"]))}
                for _, a in batch.iterrows()]
        with_ref = [dict(r, reference=questions.loc[a["question_id"], "reference_answer"])
                    for r, (_, a) in zip(base, batch.iterrows())]
        # 1) metrics that use the reference answer or the context
        res1 = evaluate(dataset=EvaluationDataset.from_list(with_ref), metrics=with_reference,
                        llm=llm, embeddings=embeddings, run_config=run_config, show_progress=True).to_pandas()
        # 2) rubric metrics without the reference answer (clarity and hallucination are not judged
        #    against the reference; hallucination is judged against the retrieved context)
        res2 = evaluate(dataset=EvaluationDataset.from_list(base), metrics=rubric_metrics,
                        llm=llm, embeddings=embeddings, run_config=run_config, show_progress=True).to_pandas()
        out = pd.DataFrame({
            "answer_id": batch["answer_id"].values,
            "technical_correctness": pick(res1, "factual_correctness"),
            "clarity": pick(res2, "clarity"),
            "faithfulness": pick(res1, "faithfulness"),
            "hallucination_control": pick(res2, "hallucination_control"),
            "answer_relevance": pick(res1, "answer_relevancy"),
            "judge_model": config.JUDGE_MODEL,
            "attempts": [attempts_before.get(i, 0) + 1 for i in batch["answer_id"]],
        })
        out.to_csv(out_path, mode="a", index=False, header=not out_path.exists())
        print(f"  saved {min(start + BATCH, len(todo))}/{len(todo)}")

    final = pd.read_csv(out_path)
    print(final[SCORE_COLUMNS].describe().round(3))
    retry_left = int((final[SCORE_COLUMNS].isna().any(axis=1) & (final["attempts"] < 2)).sum())
    print("Empty scores per criterion:", final[SCORE_COLUMNS].isna().sum().to_dict())
    if retry_left:
        print(f"{retry_left} answers have an empty score - run the same command ONCE more to retry them.")


if __name__ == "__main__":
    main()
