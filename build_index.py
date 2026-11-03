"""
STEP 3 - Splits the clean pages into chunks and creates an embedding for each chunk
(thesis Sections 3.3 and 3.4).

Chunking: max CHUNK_MAX_CHARS characters, split at sentence boundaries, neighbouring
chunks overlap by CHUNK_OVERLAP_SENTENCES sentence(s). Chunks never cross a section
heading, so every chunk belongs to exactly one section.

Run:  python build_index.py
Output: index/chunks.json, index/embeddings.npy, index/index_info.json
"""
import json
import re
from datetime import datetime

import numpy as np

import config
from llm import embed_texts

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'`(\[])")


def parse_clean_file(path):
    """Returns (title, url, list of (section_heading, block_text))."""
    text = path.read_text(encoding="utf-8")
    header, _, body = text.partition("\n\n")
    title = re.search(r"TITLE: (.*)", header).group(1)
    url = re.search(r"URL: (.*)", header).group(1)
    sections, current = [], title
    # code blocks may contain blank lines -> protect them before splitting on blank lines
    parts = re.split(r"(```.*?```)", body, flags=re.S)
    for part in parts:
        if part.startswith("```"):
            sections.append((current, part))
            continue
        for block in part.split("\n\n"):
            block = block.strip()
            if not block:
                continue
            if re.match(r"^#{1,4} ", block):
                current = block.lstrip("#").strip()
            else:
                sections.append((current, block))
    return title, url, sections


def to_units(block):
    """A unit is the smallest piece that is never split: a sentence, a list item or a code block."""
    if block.startswith("```"):
        if len(block) <= config.CHUNK_MAX_CHARS:
            return [block]
        lines, units, current = block.split("\n"), [], ""
        for line in lines:  # very long code: split between lines
            if len(current) + len(line) + 1 > config.CHUNK_MAX_CHARS and current:
                units.append(current)
                current = ""
            current += line + "\n"
        if current.strip():
            units.append(current)
        return units
    return [s.strip() for s in SENTENCE_SPLIT.split(block) if s.strip()]


def chunk_section(units):
    chunks, current = [], []
    for unit in units:
        length = sum(len(u) + 1 for u in current) + len(unit)
        if current and length > config.CHUNK_MAX_CHARS:
            chunks.append(current)
            overlap = current[-config.CHUNK_OVERLAP_SENTENCES:] if config.CHUNK_OVERLAP_SENTENCES else []
            # only overlap short sentences, never code blocks
            overlap = [u for u in overlap if not u.startswith("```") and len(u) < config.CHUNK_MAX_CHARS / 2]
            current = overlap + [unit]
        else:
            current.append(unit)
    if current:
        chunks.append(current)
    return [" ".join(c) if not any(u.startswith("```") for u in c) else "\n".join(c) for c in chunks]


def main():
    config.INDEX_DIR.mkdir(exist_ok=True)
    chunks = []
    for page in config.PAGES:
        title, url, blocks = parse_clean_file(config.CLEAN_DIR / f"{page['name']}.txt")
        # group units by section, keeping the original order
        grouped = []
        for section, block in blocks:
            if not grouped or grouped[-1][0] != section:
                grouped.append((section, []))
            grouped[-1][1].extend(to_units(block))
        for section, units in grouped:
            for text in chunk_section(units):
                chunks.append({"id": f"{page['name']}-{len(chunks):04d}", "page": page["name"],
                               "title": title, "url": url, "section": section, "text": text})
    print(f"{len(chunks)} chunks created. Creating embeddings with {config.EMBEDDING_MODEL} ...")
    # Each chunk is embedded together with its page title and section heading.
    embed_inputs = [f"{c['title']} - {c['section']}\n{c['text']}" for c in chunks]
    embeddings = embed_texts(embed_inputs)
    np.save(config.INDEX_DIR / "embeddings.npy", embeddings)
    (config.INDEX_DIR / "chunks.json").write_text(json.dumps(chunks, indent=2, ensure_ascii=False),
                                                  encoding="utf-8")
    lengths = [len(c["text"]) for c in chunks]
    info = {"embedding_model": "FAKE" if config.FAKE_MODE else config.EMBEDDING_MODEL,
            "chunk_max_chars": config.CHUNK_MAX_CHARS,
            "chunk_overlap_sentences": config.CHUNK_OVERLAP_SENTENCES,
            "n_chunks": len(chunks), "avg_chunk_chars": round(float(np.mean(lengths)), 1),
            "max_chunk_chars": int(max(lengths)),
            "chunks_per_page": {p["name"]: sum(c["page"] == p["name"] for c in chunks) for p in config.PAGES},
            "created_at": datetime.now().isoformat(timespec="seconds")}
    (config.INDEX_DIR / "index_info.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
