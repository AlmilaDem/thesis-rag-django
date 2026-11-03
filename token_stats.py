"""
Token statistics of the chunks (thesis Section 3.3).

Counts the tokens of every chunk with the tokenizer of the embedding model (all-MiniLM-L6-v2),
using exactly the text that is embedded ("title - section" + chunk text). The model reads at most
256 word pieces; longer inputs would be cut off, so the number of such chunks is reported too.

Run:  python token_stats.py
Output: index/token_stats.json (and printed on screen)
"""
import json

from sentence_transformers import SentenceTransformer

import config


def main():
    chunks = json.loads((config.INDEX_DIR / "chunks.json").read_text(encoding="utf-8"))
    model = SentenceTransformer(config.EMBEDDING_MODEL)
    limit = model.max_seq_length
    texts = [f"{c['title']} - {c['section']}\n{c['text']}" for c in chunks]
    counts = [len(model.tokenizer(t, add_special_tokens=True)["input_ids"]) for t in texts]
    text_only = [len(model.tokenizer(c["text"], add_special_tokens=True)["input_ids"]) for c in chunks]
    chars = [len(c["text"]) for c in chunks]
    stats = {
        "chunks": len(chunks),
        "embedding_model": config.EMBEDDING_MODEL,
        "model_max_seq_length": limit,
        "tokens_embedded_text_mean": round(sum(counts) / len(counts), 1),
        "tokens_embedded_text_max": max(counts),
        "tokens_embedded_text_min": min(counts),
        "tokens_chunk_text_only_mean": round(sum(text_only) / len(text_only), 1),
        "tokens_chunk_text_only_max": max(text_only),
        "chunks_over_limit": sum(n > limit for n in counts),
        "chars_mean": round(sum(chars) / len(chars), 1),
        "chars_max": max(chars),
    }
    (config.INDEX_DIR / "token_stats.json").write_text(json.dumps(stats, indent=2))
    for k, v in stats.items():
        print(f"{k:32s} {v}")


if __name__ == "__main__":
    main()
