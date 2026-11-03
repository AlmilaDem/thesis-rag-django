"""
Central configuration of the experiment.

Every value in this file is a CONTROLLED VARIABLE of the experiment (thesis Section 2.2):
it must stay the same for all questions and all strategies. Change values only during
the pilot experiment, then freeze them before the main experiment.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _load_env_file():
    """Reads KEY=VALUE lines from the .env file into environment variables."""
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file()

# If RAG_FAKE=1, no API is called: fake embeddings and fake answers are used.
# This is ONLY for checking that the scripts run. Never report fake results.
FAKE_MODE = os.environ.get("RAG_FAKE", "0") == "1"

# ---------------------------------------------------------------- corpus (Section 3.1)
DJANGO_VERSION = "5.2"
PAGES = [
    {"name": "models",     "title": "Models",
     "url": "https://docs.djangoproject.com/en/5.2/topics/db/models/"},
    {"name": "logging",    "title": "Logging",
     "url": "https://docs.djangoproject.com/en/5.2/topics/logging/"},
    {"name": "settings",   "title": "Django settings",
     "url": "https://docs.djangoproject.com/en/5.2/topics/settings/"},
    {"name": "urls",       "title": "URL dispatcher",
     "url": "https://docs.djangoproject.com/en/5.2/topics/http/urls/"},
    {"name": "deployment", "title": "Deployment checklist",
     "url": "https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/"},
]

# ---------------------------------------------------------------- folders
RAW_DIR = BASE_DIR / "corpus_raw"
CLEAN_DIR = BASE_DIR / "corpus_clean"
INDEX_DIR = BASE_DIR / "index"
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"

# ---------------------------------------------------------------- chunking (Section 3.3)
CHUNK_MAX_CHARS = 700          # max characters per chunk, split at sentence boundaries
CHUNK_OVERLAP_SENTENCES = 1    # neighbouring chunks share one sentence

# ---------------------------------------------------------------- retrieval (Section 3.4)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # runs locally on your computer, free
TOP_K = 5                      # decide with check_retrieval.py during the pilot, then freeze

# ---------------------------------------------------------------- language model (Section 3.5)
# Two answer-generating LLMs of the same family: a smaller and a larger one (fixed versions, never "-latest").
GEN_MODELS = {"3b": "ministral-3b-2512", "8b": "ministral-8b-2512"}
GEN_MODEL = GEN_MODELS["8b"]   # default for the quick manual test with rag.py
TEMPERATURE = 0
MAX_TOKENS = 1200   # raised from 800 after the pilot (3 of 108 answers were cut off)
SEED = 42

# The judge model scores the answers (Section 2.4). It is deliberately a DIFFERENT,
# stronger model than the generator, so the model does not grade its own answers.
JUDGE_MODEL = "ministral-14b-2512"

# Rate limits of your Mistral account (console.mistral.ai/limits). The scripts wait
# automatically so that these limits are not exceeded.
RATE_LIMITS = {  # model: (tokens per minute, requests per second)
    "ministral-3b-2512": (1_300_000, 12.5),
    "ministral-8b-2512": (625_000, 3.13),
    "ministral-14b-2512": (937_500, 0.5),
    "mistral-medium-2604": (20_000, 1.0),
}

# ---------------------------------------------------------------- strategies (Sections 3.6, 3.7)
BASE_INSTRUCTION = (
    "You are an assistant that answers questions about the Django "
    f"{DJANGO_VERSION} documentation. Answer the question by using the "
    "documentation excerpts given below."
)

FORMATTING = {
    "F0": "",  # baseline: no formatting instruction
    "F1": "Answer in one short paragraph of 3-5 sentences. Do not use lists or headings.",
    "F2": "Answer as numbered steps in the order in which they should be performed.",
}

REFUSAL_SENTENCE = "The answer cannot be found in the provided documentation."

GROUNDING = {
    "G0": "",  # baseline: no grounding instruction
    "G1": "After each claim, add the number of the chunk that supports it in square "
          "brackets, for example [1].",
    "G2": "Use only the information in the provided documentation. If the answer is "
          f"not in the documentation, say: '{REFUSAL_SENTENCE}'",
}

# ---------------------------------------------------------------- scoring (Section 2.4)
CRITERIA = ["technical_correctness", "clarity", "faithfulness",
            "hallucination_control", "answer_relevance"]

# Share of judged answers that the external reviewer scores by hand.
HUMAN_SAMPLE_SHARE = 0.20
