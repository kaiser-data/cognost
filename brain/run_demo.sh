#!/usr/bin/env bash
# End-to-end demo of the BrainFlow Company Brain: ingest -> query -> self-improve -> query -> lint.
# Run from the Cognost/ project root with the venv active.
set -euo pipefail
cd "$(dirname "$0")/.."
source .venv/bin/activate

echo "════════ STEP 1 · INGEST ════════"
python brain/ingest.py --reset --raw-only

echo; echo "════════ STEP 2 · QUERY (before — baseline skill, naive RAG) ════════"
python brain/query.py --skill archive/wiki-maintainer.v1-baseline --tag before --mode rag

echo; echo "════════ STEP 2 · SELF-IMPROVE (distill + propose) ════════"
python brain/selfimprove.py --from-tag before
PROPOSAL=$(ls -t brain/proposals/wiki-maintainer.*.md | grep -v rationale | head -1)
echo "Applying proposal: $(basename "$PROPOSAL")"
python brain/selfimprove.py --apply "$(basename "$PROPOSAL")"

echo; echo "════════ STEP 2 · QUERY (after — improved skill, graph memory) ════════"
python brain/query.py --tag after --mode graph

echo; echo "════════ Self-improvement evidence ════════"
python brain/evidence.py

echo; echo "════════ STEP 3 · LINT ════════"
python brain/lint.py || true
echo; echo "✓ demo complete — see brain/evidence/"
