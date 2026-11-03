"""
STEP 1 - Downloads the selected Django 5.2 documentation pages as HTML (raw corpus).

Run:  python download_docs.py
Output: corpus_raw/<page>.html  and  corpus_raw/download_log.json
"""
import json
import time
from datetime import datetime

import requests

import config


def main():
    config.RAW_DIR.mkdir(exist_ok=True)
    log = []
    for page in config.PAGES:
        print(f"Downloading {page['url']} ...")
        response = requests.get(page["url"], timeout=30,
                                headers={"User-Agent": "Mozilla/5.0 (bachelor thesis research)"})
        response.raise_for_status()
        path = config.RAW_DIR / f"{page['name']}.html"
        path.write_text(response.text, encoding="utf-8")
        log.append({"name": page["name"], "url": page["url"], "status": response.status_code,
                    "bytes": len(response.content),
                    "downloaded_at": datetime.now().isoformat(timespec="seconds")})
        time.sleep(1)  # be polite to the server
    (config.RAW_DIR / "download_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"Done. {len(log)} pages saved to {config.RAW_DIR}")


if __name__ == "__main__":
    main()
