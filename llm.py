"""
Wrapper for the two models the system uses:
  - embeddings: a local sentence-transformers model (free, runs on your computer)
  - chat (answers and judge): the Mistral API
Includes automatic retries (rate limits) and a fake mode for free test runs.
"""
import hashlib
import json
import os
import re
import time

import numpy as np

import config

_client = None
_embedder = None
_last_call = {}  # model -> (time of last call, tokens it used)


def _get_client():
    global _client
    if _client is None:
        try:
            from mistralai.client import Mistral   # mistralai v2 / v3
        except ImportError:
            from mistralai import Mistral          # mistralai v1
        key = os.environ.get("MISTRAL_API_KEY", "")
        if not key or key.startswith("paste-"):
            raise SystemExit("MISTRAL_API_KEY is missing. Put it into the .env file.")
        _client = Mistral(api_key=key)
    return _client


def _with_retries(func, *args, **kwargs):
    """Retries an API call up to 8 times (free-tier rate limits, network errors)."""
    for attempt in range(8):
        try:
            return func(*args, **kwargs)
        except Exception as error:  # noqa: BLE001
            if attempt == 7:
                raise
            wait = min(60, 2 ** (attempt + 1))
            print(f"  API error ({error.__class__.__name__}: {str(error)[:120]}). Retrying in {wait}s...")
            time.sleep(wait)


# ---------------------------------------------------------------- embeddings
def _fake_embedding(text, dim=512):
    vector = np.zeros(dim, dtype=np.float32)
    for word in re.findall(r"[a-z0-9_]+", text.lower()):
        vector[int(hashlib.md5(word.encode()).hexdigest(), 16) % dim] += 1.0
    return vector


def embed_texts(texts):
    """Returns an (n, d) array of L2-normalised embeddings (dot product == cosine similarity)."""
    global _embedder
    if config.FAKE_MODE:
        vectors = np.array([_fake_embedding(t) for t in texts])
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vectors / norms
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer(config.EMBEDDING_MODEL)
    return np.asarray(_embedder.encode(texts, normalize_embeddings=True,
                                       show_progress_bar=len(texts) > 50), dtype=np.float32)


# ---------------------------------------------------------------- chat
def _throttle(model):
    """Waits long enough after the previous call to stay under the account's rate limits."""
    if model not in _last_call:
        return
    tokens_per_minute, requests_per_second = config.RATE_LIMITS.get(model, (20_000, 1.0))
    last_time, last_tokens = _last_call[model]
    needed = max(1.0 / requests_per_second + 0.1, last_tokens / tokens_per_minute * 60)
    remaining = needed - (time.time() - last_time)
    if remaining > 0:
        time.sleep(remaining)


def _fake_chat(messages, json_mode):
    prompt = messages[-1]["content"]
    seed = int(hashlib.md5(prompt.encode()).hexdigest(), 16)
    if json_mode:
        return json.dumps({c: {"score": 1 + (seed >> (i * 3)) % 5, "reason": "fake"}
                           for i, c in enumerate(config.CRITERIA)})
    excerpt = re.search(r"\[1\][^\n]*\n(.+?)(\n\n|$)", prompt, re.S)
    text = excerpt.group(1)[:200] if excerpt else "Django is a web framework."
    cite = " [1]" if "square brackets" in prompt else ""
    if "numbered steps" in prompt:
        return f"1. {text}{cite}\n2. Save the file.{cite}\n3. Restart the server.{cite}"
    if "Use only the information" in prompt and seed % 4 == 0:
        return config.REFUSAL_SENTENCE
    return f"{text}{cite} This is a fake answer. It is used only for testing. It has no value."


def chat(messages, model, temperature=0, max_tokens=800, json_mode=False):
    """Returns (answer_text, metadata_dict)."""
    if config.FAKE_MODE:
        return _fake_chat(messages, json_mode), {"model": "FAKE", "system_fingerprint": None,
                                                 "prompt_tokens": 0, "completion_tokens": 0}
    _throttle(model)
    kwargs = dict(model=model, messages=messages, temperature=temperature,
                  max_tokens=max_tokens, random_seed=config.SEED)
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = _with_retries(_get_client().chat.complete, **kwargs)
    usage = getattr(response, "usage", None)
    _last_call[model] = (time.time(), getattr(usage, "total_tokens", None) or 2500)
    meta = {"model": getattr(response, "model", model), "system_fingerprint": None,
            "prompt_tokens": getattr(usage, "prompt_tokens", None),
            "completion_tokens": getattr(usage, "completion_tokens", None)}
    return str(response.choices[0].message.content).strip(), meta
