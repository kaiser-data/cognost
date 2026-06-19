"""Step 1 — INGEST.

Pull BrainFlow's scattered team knowledge into the permanent graph:
  - the 12 immutable source documents in raw/   (what was said, by whom)
  - the synthesized wiki/ pages                  (the distilled, cited, conflict-aware knowledge)

Idempotent: re-running with --reset prunes first so ingest converges to the same state
(CLAUDE.md §3.5). Optionally pushes the dataset to a Cognee Cloud instance for the bonus.

    python brain/ingest.py            # add + cognify into the local permanent graph
    python brain/ingest.py --reset    # prune everything first, then ingest
    python brain/ingest.py --memify   # also run memory-enrichment algorithms
    python brain/ingest.py --push     # push the dataset to Cognee Cloud (needs env below)
"""
from __future__ import annotations

import argparse
import asyncio
import os

import cognee

from common import DATASET, RAW_DIR, WIKI_DIR


def _docs(raw_only: bool = False) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    for p in sorted(RAW_DIR.glob("*.md")):
        if p.name.lower() == "readme.md":      # README is the cheat-sheet, not a source
            continue
        items.append((f"raw/{p.name}", p.read_text(encoding="utf-8")))
    if not raw_only:
        for p in sorted(WIKI_DIR.rglob("*.md")):
            rel = p.relative_to(WIKI_DIR.parent)
            items.append((str(rel), p.read_text(encoding="utf-8")))
    return items


async def main(reset: bool, do_memify: bool, do_push: bool, raw_only: bool) -> None:
    if reset:
        print("· pruning existing data + system metadata …")
        await cognee.prune.prune_data()
        await cognee.prune.prune_system(metadata=True)

    docs = _docs(raw_only)
    print(f"· adding {len(docs)} documents to dataset '{DATASET}' …")
    for name, text in docs:
        # Prefix each doc with its provenance so the graph keeps source identity.
        await cognee.add(f"# SOURCE: {name}\n\n{text}", dataset_name=DATASET)
        print(f"    + {name}")

    print("· cognify: building entities, relationships, summaries …")
    await cognee.cognify(datasets=[DATASET])

    if do_memify:
        print("· memify: running memory-enrichment algorithms …")
        await cognee.memify(dataset=DATASET)

    if do_push:
        url = os.getenv("COGNEE_CLOUD_URL")
        key = os.getenv("COGNEE_CLOUD_API_KEY")
        if not (url and key):
            print("! --push set but COGNEE_CLOUD_URL / COGNEE_CLOUD_API_KEY are missing; skipping.")
        else:
            print(f"· pushing dataset '{DATASET}' to Cognee Cloud …")
            res = await cognee.push(dataset=DATASET, url=url, api_key=key)
            print(f"    pushed: {res}")

    print("✓ ingest complete — permanent graph built.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--reset", action="store_true", help="prune all data first (idempotent rebuild)")
    ap.add_argument("--memify", action="store_true", help="run memory-enrichment algorithms after cognify")
    ap.add_argument("--push", action="store_true", help="push dataset to Cognee Cloud")
    ap.add_argument("--raw-only", action="store_true", help="ingest only raw/ (fast demo path)")
    args = ap.parse_args()
    asyncio.run(main(args.reset, args.memify, args.push, args.raw_only))
