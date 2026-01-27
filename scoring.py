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

def get_player_stats(name):
    scores = load_scores()
    player_scores = [s for s in scores if s["name"].lower() == name.lower()]

    if not player_scores:
        return None

    stats = {"games": len(player_scores), "categories": {}}
    total_correct = 0
    total_questions = 0

    for s in player_scores:
        cat = s["category"]
        if cat not in stats["categories"]:
            stats["categories"][cat] = {"correct": 0, "total": 0, "games": 0}
        stats["categories"][cat]["correct"] += s["score"]
        stats["categories"][cat]["total"] += s["total"]
        stats["categories"][cat]["games"] += 1
        total_correct += s["score"]
        total_questions += s["total"]

    stats["total_correct"] = total_correct
    stats["total_questions"] = total_questions

    return stats
