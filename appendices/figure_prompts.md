# Prompts Used to Create the Figures

Figures 4.1 and 5.1–5.3 of the thesis were created with Claude (Anthropic, Claude Opus 5.5) using the prompts below. The numbers in Figures 5.1 and 5.3 come from the result files that were attached to the prompt; the numbers for Figure 5.2 are given in the prompt itself.

| Figure | Content | Attached file |
|---|---|---|
| [Fig. 4.1](#fig-41--architecture-of-the-rag-system) | Architecture of the RAG system | – |
| [Fig. 5.1](#fig-51--differences-between-the-formatting-strategies) | Differences between the formatting strategies | [`extra_formatting_effects_all.csv`](../results/final/tables/extra_formatting_effects_all.csv) |
| [Fig. 5.2](#fig-52--answers-to-the-unanswerable-questions) | Answers to the unanswerable questions | – (numbers in the prompt) |
| [Fig. 5.3](#fig-53--overall-score-by-question-type) | Overall score by question type | [`RQ3_type_x_condition_overall_all.csv`](../results/final/tables/RQ3_type_x_condition_overall_all.csv) |

---

## Fig. 4.1 – Architecture of the RAG system

> I am writing my bachelor thesis about a RAG-based question answering system over the Django documentation, and I need a diagram of the system architecture for Chapter 4. Please draw it in black, white and grey so that it looks good in a printed thesis.
>
> The system works in three stages, and I would like to show them as three horizontal bands from top to bottom: indexing, answering and evaluation. Indexing is done only once before the experiment: I download five pages of the Django 5.2 documentation, clean the HTML, split the text into 240 chunks and create embeddings with all-MiniLM-L6-v2. In the answering stage, a question from my question set (25 answerable and 10 unanswerable questions) is used to retrieve the five most similar chunks, a prompt is built with the question, the chunks and the formatting and grounding instructions, and two LLMs (ministral-3b-2512 and ministral-8b-2512) generate the answers. In total there are 630 answers. In the evaluation stage, all answers are checked with simple rules, the 450 answers to the answerable questions are scored with RAGAS (evaluator ministral-14b-2512), 90 answers are scored by an external reviewer and compared with RAGAS, and at the end everything is analysed with tables, statistical tests and figures.
>
> Please show each step as a box with the name of my script (download_docs.py, clean_docs.py, build_index.py, auto_checks.py, ragas_eval.py, human_sample.py and agreement.py, analyze.py) and a short explanation, connect the steps with arrows, and make the index and the 630 answers look different from the steps, because they are data and not steps. The diagram should fit the width of an A4 page.

---

## Fig. 5.1 – Differences between the formatting strategies

> I compared three answer formatting strategies in my thesis: F0 (no instruction), F1 (short paragraph) and F2 (step-by-step). I attached a file with the results of the pairwise comparisons (F0 vs F1, F0 vs F2, F1 vs F2) for technical correctness, faithfulness, answer relevance and the overall score. For each pair it contains the mean difference, the 95 % bootstrap confidence interval and the Holm-corrected p-value.
>
> Can you make a figure that shows, for each criterion, the mean differences of the three pairs with their confidence intervals, so that the reader can see at a glance which differences are clearly different from zero? Please mark the differences that are significant after the Holm correction (p < 0.05) differently from the others, and add a line at zero. It is for a printed thesis, so please use only black, white and grey and Times New Roman.

---

## Fig. 5.2 – Answers to the unanswerable questions

> In my thesis I classified the answers to the questions whose answers are not in the documentation into three classes: (a) correct refusal, (b) partial refusal (the LLM says the information is missing but still answers) and (c) unsupported answer. I want a figure that compares the three grounding strategies (G0 no instruction, G1 inline citations, G2 source-restricted answering) and the two LLMs (3b and 8b). Each group has 30 answers. The numbers are (a, b, c):
>
> | Strategy | LLM | (a) | (b) | (c) |
> |---|---|---|---|---|
> | G0 | 3b | 0 | 19 | 11 |
> | G0 | 8b | 0 | 16 | 14 |
> | G1 | 3b | 2 | 17 | 11 |
> | G1 | 8b | 2 | 15 | 13 |
> | G2 | 3b | 17 | 12 | 1 |
> | G2 | 8b | 21 | 9 | 0 |
>
> The main point of the figure should be that almost only G2 leads to correct refusals. Please show the number of answers in each part of the figure, keep the two LLMs of the same strategy next to each other, and use only black, white and grey and Times New Roman, because it is for a printed thesis.

---

## Fig. 5.3 – Overall score by question type

> I attached a table with the mean overall score (0–1) of each of my nine strategy combinations (F0+G0 to F2+G2) for each of the five question types (definition, how-to, troubleshooting, configuration and API usage). I would like a figure that shows all these values at once, so that the reader can see which combination works best for each question type. Please write the values in the figure and highlight the best combination of each question type. It is for a printed thesis, so please use greyscale and Times New Roman.
