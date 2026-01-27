import json
import os
from datetime import datetime

SCORES_FILE = os.path.join(os.path.dirname(__file__), "data", "scores.json")

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r") as f:
        return json.load(f)

def save_score(name, score, total, category):
    scores = load_scores()
    scores.append({
        "name": name,
        "score": score,
        "total": total,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=2)

def get_top_scores(limit=5):
    scores = load_scores()
    scores.sort(key=lambda s: s["score"], reverse=True)
    return scores[:limit]
