"""Canonical demo queries — each hits a planted misalignment (see raw/README.md cheat sheet).

expect_terms : facts a *complete* answer should contain.
expect_conflict : True when the honest answer must surface a disagreement / supersession.
"""

QUERIES = [
    {"issue": "B", "q": "What's the current premium-upgrade timing, and was it ever changed?",
     "expect_terms": ["Day 7", "Day 3", "reverted"], "expect_conflict": True},
    {"issue": "A", "q": "Is the AI Daily Pick part of the MVP?",
     "expect_terms": ["Won't have", "PRD", "Roadmap"], "expect_conflict": True},
    {"issue": "C", "q": "What does the HR dashboard show employers?",
     "expect_terms": ["anonymised", "by name", "Sales"], "expect_conflict": True},
    {"issue": "D", "q": "What is our retention target?",
     "expect_terms": ["30-day", "7-day", "40%"], "expect_conflict": True},
    {"issue": "E", "q": "Which platform do we launch on first?",
     "expect_terms": ["simultaneous", "iOS", "Android"], "expect_conflict": True},
    {"issue": "F", "q": "What backend are we using?",
     "expect_terms": ["Supabase", "Firebase", "EU"], "expect_conflict": True},
    {"issue": "G", "q": "What does BrainFlow Premium cost?",
     "expect_terms": ["4.99", "3.99"], "expect_conflict": True},
]
