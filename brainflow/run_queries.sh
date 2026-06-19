#!/usr/bin/env bash
# Run the demo money-shot suite + decoy precision checks against the live brainflow brain.
set -u
BF_ID="2b6f9b6d-8a07-5ab1-9488-3ffbb1279fa7"   # brainflow dataset
SID=$(cat /private/tmp/claude-501/-Users-marty-claude-projects-hackathon-cognee-secondbrain/fe3c1202-7c2a-4cc1-a752-26f273710696/scratchpad/cognee_session_id 2>/dev/null)
OUT=/Users/marty/claude-projects/hackathon/cognee-secondbrain/brainflow/snapshots/query-results.json
echo "[" > "$OUT"
first=1

ask () {
  local id="$1"; local kind="$2"; local q="$3"
  echo ">>> [$id] $q"
  local resp
  resp=$(curl -s -X POST "$COGNEE_BASE_URL/api/v1/recall" \
    -H "X-Api-Key: $COGNEE_API_KEY" -H "Content-Type: application/json" \
    -d "{\"query\": $(python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$q"), \"dataset_name\": \"brainflow\", \"session_id\": \"$SID\"}")
  # extract only the brainflow dataset answer
  local ans
  ans=$(echo "$resp" | BF="$BF_ID" python3 -c "
import sys,json,os
bf=os.environ['BF']
try:
    d=json.load(sys.stdin)
    hit=[r for r in d if r.get('dataset_id')==bf]
    print(hit[0]['text'] if hit else (d[0]['text'] if d else '(no answer)'))
except Exception as e:
    print('(parse error: %s)'%e)
")
  echo "$ans"
  echo "-------------------------------------------------------------------"
  [ $first -eq 0 ] && echo "," >> "$OUT"
  first=0
  python3 -c "
import json,sys
print(json.dumps({'id':sys.argv[1],'kind':sys.argv[2],'query':sys.argv[3],'answer':sys.argv[4]}, ensure_ascii=False))
" "$id" "$kind" "$q" "$ans" >> "$OUT"
}

ask A money "Is the AI Daily Pick part of the MVP scope? Cite sources and surface any disagreement."
ask C money "What does the B2B HR dashboard show employers about individual employees? Cite sources."
ask E money "Which platform does BrainFlow launch on first - iOS, Android, or both? Cite sources and note conflicts."
ask F money "What backend is BrainFlow using, and was it ever changed? State current vs superseded."
ask G money "What does BrainFlow Premium cost per month? Cite sources and surface any disagreement."
ask D money "What is BrainFlow's retention target and exactly how is it defined?"
ask H money "How long is a single guided exercise in BrainFlow? Cite sources."
ask SCOPE money "Does the current design spec match the PRD scope? List every mismatch with citations."
ask DECOY_PRICE precision "Is BrainFlow itself priced at 3.99 euro per month, or is that a competitor's price?"
ask DECOY_AMPLITUDE precision "Is BrainFlow currently using Amplitude for analytics, or was that decision superseded?"
ask DECOY_DRAFT precision "Is BrainFlow officially targeting 50,000 monthly active users?"

echo "]" >> "$OUT"
echo "ALL DONE -> $OUT"
