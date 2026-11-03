"""
The RAG system: retrieval, prompt building and answer generation (thesis Chapter 4).

Quick test from the terminal:
    python rag.py "What is a Django model?"
    python rag.py "How is reverse() used?" --f F2 --g G1
"""
import argparse
import json
from functools import lru_cache

import numpy as np

import config
from llm import chat, embed_texts


@lru_cache(maxsize=1)
def load_index():
    chunks = json.loads((config.INDEX_DIR / "chunks.json").read_text(encoding="utf-8"))
    embeddings = np.load(config.INDEX_DIR / "embeddings.npy")
    return chunks, embeddings


def retrieve(question, k=config.TOP_K):
    """Returns the k most similar chunks (cosine similarity) with their scores."""
    chunks, embeddings = load_index()
    query = embed_texts([question])[0]
    scores = embeddings @ query                 # vectors are normalised -> cosine similarity
    best = np.argsort(-scores)[:k]
    return [{**chunks[i], "score": round(float(scores[i]), 4), "rank": r + 1}
            for r, i in enumerate(best)]


def build_messages(question, retrieved, formatting_code, grounding_code):
    """Builds the prompt. Only the formatting and grounding instructions differ between strategies."""
    excerpts = "\n\n".join(
        f"[{n}] ({c['title']} - {c['section']})\n{c['text']}" for n, c in enumerate(retrieved, 1))
    parts = [config.BASE_INSTRUCTION, "", "Documentation excerpts:", excerpts, "",
             f"Question: {question}"]
    instructions = [config.FORMATTING[formatting_code], config.GROUNDING[grounding_code]]
    instructions = [i for i in instructions if i]
    if instructions:
        parts += ["", "Instructions:"] + [f"- {i}" for i in instructions]
    return [{"role": "user", "content": "\n".join(parts)}]


def generate(question, retrieved, formatting_code="F0", grounding_code="G0", model=None):
    messages = build_messages(question, retrieved, formatting_code, grounding_code)
    answer, meta = chat(messages, model=model or config.GEN_MODEL, temperature=config.TEMPERATURE,
                        max_tokens=config.MAX_TOKENS)
    return answer, messages, meta


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--f", default="F0", choices=config.FORMATTING)
    parser.add_argument("--g", default="G0", choices=config.GROUNDING)
    parser.add_argument("--k", type=int, default=config.TOP_K)
    parser.add_argument("--llm", default="8b", choices=config.GEN_MODELS)
    args = parser.parse_args()
    found = retrieve(args.question, args.k)
    print("Retrieved chunks:")
    for c in found:
        print(f"  [{c['rank']}] {c['score']:.3f}  {c['page']} / {c['section']}")
    answer, _, meta = generate(args.question, found, args.f, args.g, config.GEN_MODELS[args.llm])
    print(f"\nAnswer ({args.f}, {args.g}, model={meta['model']}):\n{answer}")
