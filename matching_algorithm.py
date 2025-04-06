from difflib import SequenceMatcher

def calculate_match_score(jd_summary, cv_summary):
    return round(SequenceMatcher(None, jd_summary, cv_summary).ratio() * 100, 2)
