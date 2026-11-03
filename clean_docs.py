"""
STEP 2 - Cleans the raw HTML pages (clean corpus, thesis Section 3.2).

Keeps headings, paragraphs, lists, tables and code examples.
Removes navigation, headers/footers, sidebars, version links, scripts.

Run:  python clean_docs.py
Output: corpus_clean/<page>.txt  and  corpus_clean/corpus_stats.json (values for Table 3.2)
"""
import json
import re

from bs4 import BeautifulSoup, NavigableString, Tag

import config

REMOVE_SELECTORS = ["script", "style", "nav", "header", "footer", "aside", "form",
                    "a.headerlink", "#doc-versions", ".nav-breadcrumbs", ".browse-horizontal",
                    "#billboard", ".footer", ".sidebar", "#docs-version-switcher"]
HEADINGS = {"h1": "#", "h2": "##", "h3": "###", "h4": "####"}


def clean_text(text):
    text = text.replace("¶", "")           # pilcrow sign of heading anchors
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub(r"\s+([.,;:!?)\]])", r"\1", text)   # "features ." -> "features."


def walk(node, blocks):
    """Visits the HTML tree in reading order and collects content blocks."""
    for child in node.children:
        if isinstance(child, NavigableString) or not isinstance(child, Tag):
            continue
        name = child.name
        if name in HEADINGS:
            text = clean_text(child.get_text(" "))
            if text:
                blocks.append(f"{HEADINGS[name]} {text}")
        elif name == "pre":
            code = child.get_text().rstrip()
            if code.strip():
                blocks.append(f"```\n{code}\n```")
        elif name in ("p", "dt", "dd"):
            if child.find(["pre", "ul", "ol", "table"]):
                walk(child, blocks)
            else:
                text = clean_text(child.get_text(" "))
                if text:
                    blocks.append(text)
        elif name == "li":
            if child.find(["p", "pre", "ul", "ol"]):
                walk(child, blocks)
            else:
                text = clean_text(child.get_text(" "))
                if text:
                    blocks.append(f"- {text}")
        elif name == "table":
            for row in child.find_all("tr"):
                cells = [clean_text(c.get_text(" ")) for c in row.find_all(["th", "td"])]
                if any(cells):
                    blocks.append(" | ".join(cells))
        else:
            walk(child, blocks)


def clean_page(html):
    soup = BeautifulSoup(html, "html.parser")
    content = (soup.select_one("#docs-content") or soup.find("article")
               or soup.find("main") or soup.body or soup)
    for selector in REMOVE_SELECTORS:
        for element in content.select(selector):
            element.decompose()
    blocks = []
    walk(content, blocks)
    return blocks


def main():
    config.CLEAN_DIR.mkdir(exist_ok=True)
    stats = {"pages": []}
    for page in config.PAGES:
        raw_path = config.RAW_DIR / f"{page['name']}.html"
        html = raw_path.read_text(encoding="utf-8")
        blocks = clean_page(html)
        header = f"TITLE: {page['title']}\nURL: {page['url']}\n\n"
        text = header + "\n\n".join(blocks) + "\n"
        (config.CLEAN_DIR / f"{page['name']}.txt").write_text(text, encoding="utf-8")
        stats["pages"].append({"name": page["name"], "raw_chars": len(html),
                               "clean_chars": len(text), "blocks": len(blocks)})
        print(f"{page['name']}: {len(html):,} raw chars -> {len(text):,} clean chars")
    pages = stats["pages"]
    stats["raw_total_chars"] = sum(p["raw_chars"] for p in pages)
    stats["clean_total_chars"] = sum(p["clean_chars"] for p in pages)
    stats["avg_clean_page_chars"] = round(stats["clean_total_chars"] / len(pages))
    (config.CLEAN_DIR / "corpus_stats.json").write_text(json.dumps(stats, indent=2),
                                                         encoding="utf-8")
    print("Corpus statistics (Table 3.2) saved to corpus_clean/corpus_stats.json")
    print("IMPORTANT: open the .txt files and check by eye that no menu/footer text is left.")


if __name__ == "__main__":
    main()
