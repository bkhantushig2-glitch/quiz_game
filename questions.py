import json
import random
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "questions.json")

def load_questions():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def get_categories():
    data = load_questions()
    return list(data.keys())

def get_point_values():
    return [200, 400, 600, 800, 1000]

def get_questions(category, difficulty=None):
    data = load_questions()
    questions = data[category]
    if difficulty:
        questions = [q for q in questions if q.get("difficulty") == difficulty]
    random.shuffle(questions)
    return questions

def build_board():
    data = load_questions()
    categories = list(data.keys())
    point_values = get_point_values()
    board = {}

    for cat in categories:
        board[cat] = {}
        for pts in point_values:
            pool = [q for q in data[cat] if q["points"] == pts]
            random.shuffle(pool)
            if pool:
                board[cat][pts] = pool[0]

    return board
