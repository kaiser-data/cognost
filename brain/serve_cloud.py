"""Cognee Cloud bonus — connect the SDK to Cognee Cloud via cognee.serve(), then run the
same remember / recall the local pipeline uses, but routed to the cloud instance.

    python brain/serve_cloud.py --recall "What is the current paywall timing?"
    python brain/serve_cloud.py --push-raw        # push the raw/ corpus to the cloud brain

Reads COGNEE_BASE_URL (or COGNEE_SERVICE_URL) and COGNEE_API_KEY from .env. With a direct URL,
serve() skips Auth0 and connects straight to the tenant; all operations then route to the cloud.
"""
from __future__ import annotations

import argparse
import asyncio
import glob
import os

import cognee

from common import DATASET, RAW_DIR, extract_answer


async def connect():
    url = os.getenv("COGNEE_SERVICE_URL") or os.getenv("COGNEE_BASE_URL")
    api_key = os.getenv("COGNEE_API_KEY", "")
    if not url:
        raise SystemExit("Set COGNEE_BASE_URL (or COGNEE_SERVICE_URL) and COGNEE_API_KEY in .env")
    # Direct mode: url + api_key → no Auth0, connect straight to the tenant.
    client = await cognee.serve(url=url, api_key=api_key)
    print(f"· connected to Cognee Cloud — all operations now route to {url}")
    return client


async def push_raw():
    await connect()
    paths = sorted(glob.glob(str(RAW_DIR / "*.md")))
    print(f"· pushing {len(paths)} raw docs to cloud dataset '{DATASET}' …")
    for p in paths:
        await cognee.remember(open(p, encoding="utf-8").read(), dataset_name=DATASET)
        print("   +", os.path.basename(p))
    print("✓ pushed. The cloud brain is built.")


async def recall(query: str):
    await connect()
    res = await cognee.recall(query_text=query, dataset_name=DATASET)
    answer, _ = extract_answer(res)
    print("\nQ:", query)
    print("A:", answer)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--recall", metavar="QUERY", help="ask the cloud brain a question")
    ap.add_argument("--push-raw", action="store_true", help="push raw/ corpus to the cloud brain")
    args = ap.parse_args()
    if args.push_raw:
        asyncio.run(push_raw())
    elif args.recall:
        asyncio.run(recall(args.recall))
    else:
        asyncio.run(connect())
