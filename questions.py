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

def get_difficulties():
    return ["easy", "medium", "hard"]

def get_questions(category, difficulty=None):
    data = load_questions()
    questions = data[category]
    if difficulty:
        questions = [q for q in questions if q["difficulty"] == difficulty]
    random.shuffle(questions)
    return questions
