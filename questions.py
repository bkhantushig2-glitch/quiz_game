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

def get_questions(category):
    data = load_questions()
    questions = data[category]
    random.shuffle(questions)
    return questions
