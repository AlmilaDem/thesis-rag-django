"""Helpers for reading questions and result files."""
import json

import pandas as pd

import config

QUESTION_COLUMNS = ["id", "type", "answerable", "question", "reference_answer",
                    "expected_page", "expected_section"]


def load_questions(question_set):
    path = config.DATA_DIR / f"questions_{question_set}.csv"
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing = [c for c in QUESTION_COLUMNS if c not in df.columns]
    if missing:
        raise SystemExit(f"{path} is missing columns: {missing}")
    df["answerable"] = df["answerable"].str.strip().str.lower().isin(["yes", "y", "true", "1"])
    todo = df[df["question"].str.contains("TODO") |
              (df["answerable"] & df["reference_answer"].str.contains("TODO"))]
    if len(todo):
        print(f"WARNING: {len(todo)} question(s) still contain TODO: {list(todo['id'])}")
    return df


def results_dir(question_set):
    path = config.RESULTS_DIR / question_set
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_retrieved(question_set):
    path = results_dir(question_set) / "retrieved.json"
    return json.loads(path.read_text(encoding="utf-8"))


def source_hit(retrieved_chunks, expected_page, expected_section):
    """Checks whether the expected source is among the retrieved chunks."""
    page_hit = any(c["page"] == expected_page for c in retrieved_chunks)
    if not expected_section or expected_section.startswith("TODO"):
        return page_hit, None
    section_hit = any(c["page"] == expected_page and
                      expected_section.strip().lower() == c["section"].strip().lower()
                      for c in retrieved_chunks)
    return page_hit, section_hit
