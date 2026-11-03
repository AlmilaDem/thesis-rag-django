# RAG answer formatting × source grounding on Django 5.2 documentation

Code, data and results of the bachelor thesis **“Comparative Evaluation of Answer Formatting and Source Grounding Strategies for RAG-Based Question Answering over Software Documentation”** (Almila Demir, Riga Technical University, 2026–2027).

The experiment compares three formatting strategies (F0 baseline, F1 short paragraph, F2 step-by-step) and three grounding strategies (G0 baseline, G1 inline citations, G2 source-restricted answering) in a RAG system over five pages of the Django 5.2 documentation, with two LLMs (ministral-3b-2512, ministral-8b-2512). The answers are evaluated with RAGAS 0.2.15 (evaluator: ministral-14b-2512).

## Online appendices of the thesis

| Thesis appendix | Location in this repository |
|---|---|
| Appendix 1. Question set with reference answers and expected sources | [`data/`](data/) |
| Appendix 2. Prompt templates | [`config.py`](config.py) (instructions), [`rag.py`](rag.py) (prompt structure), [`results/final/prompts.jsonl`](results/final/prompts.jsonl) (all 630 prompts) |
| Appendix 3. Scoring rubric and scoring form | [`ragas_eval.py`](ragas_eval.py) (rubric descriptions), [`results/final/human_scoring_form.xlsx`](results/final/human_scoring_form.xlsx) |
| Appendix 4. Additional results and generated answers | [`results/`](results/) |
| Appendix 5. Source code | this repository |
| Appendix 6. Use of AI tools | [`appendices/`](appendices/) |

## Repository structure

```
config.py              all fixed settings (pages, chunking, k, LLMs, temperature, seed, prompt instructions)
download_docs.py       1  downloads the five Django 5.2 pages
clean_docs.py          2  removes navigation etc.            -> corpus_clean/
build_index.py         3  chunks + embeddings                 -> index/
token_stats.py            tokens per embedded chunk           -> index/token_stats.json
check_retrieval.py     4  expected source for k = 1,3,5,7,10 (pilot)
run_experiment.py      5  retrieval once per question + all answers -> answers.csv, prompts.jsonl
auto_checks.py         6  format / citation / refusal-sentence checks
ragas_eval.py          7  RAGAS scores (5 criteria)
variability.py            5 questions × 9 strategies × 2 LLMs × 5 repeats
human_sample.py        8  blind form for the external reviewer
agreement.py           9  manual vs. RAGAS agreement
analyze.py            10  result tables and statistical tests
stats_extra.py        11  effect sizes, bootstrap CIs, Holm across criteria, interaction test, weight sensitivity
make_figs.py          12  Figures 5.1–5.3 of the thesis
rag.py, llm.py, experiment_io.py   helper modules
data/                  questions_pilot.csv, questions_final.csv
results/pilot_single_model/   pilot experiment of Section 5.1 (ministral-8b-2512, 108 answers)
results/final/         main experiment (630 answers), variability test, tables, refusal classification
figures/               Figures 5.1–5.3
appendices/            prompts used with AI tools
```

## How to run

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # experiment
pip install -r requirements-ragas.txt    # RAGAS evaluation
cp .env.example .env                     # then paste your own Mistral API key into .env
```

Run the scripts in the order above, first with `--set pilot`, then with `--set final`. The API key is not part of this repository.

## Notes on the data

- `results/final/prompts.jsonl` and `results/final/retrieved.json` contain excerpts of the Django 5.2 documentation (© Django Software Foundation and individual contributors, https://docs.djangoproject.com/en/5.2/). The full pages are not redistributed here; they can be downloaded again with `download_docs.py`.
- `results/final/refusal_classification/` contains the classification of the 180 answers to the unanswerable questions into (a) correct refusal, (b) partial refusal and (c) unsupported answer, made by the author without seeing the strategy or the LLM (Section 4.5).
- The key of the blind manual scoring form is not published until the external reviewer has finished the scoring.
