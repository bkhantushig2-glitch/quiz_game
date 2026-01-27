def show_welcome():
    print()
    print("=" * 40)
    print("        QUIZ GAME")
    print("=" * 40)
    print()

def show_menu(categories):
    print("Pick a category:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat.title()}")
    print(f"  {len(categories) + 1}. Leaderboard")
    print(f"  {len(categories) + 2}. Quit")
    print()

def show_question(num, total, q):
    print(f"\nQuestion {num}/{total}")
    print(f"  {q['question']}")
    for i, option in enumerate(q["options"], 1):
        print(f"    {i}. {option}")

def show_result(correct, answer):
    if correct:
        print("  Correct!")
    else:
        print(f"  Wrong! The answer was: {answer}")

def show_final_score(score, total):
    print()
    print("-" * 30)
    print(f"  You got {score}/{total}")
    if score == total:
        print("  Perfect score!")
    elif score >= total / 2:
        print("  Nice job!")
    else:
        print("  Better luck next time!")
    print("-" * 30)

def show_leaderboard(scores):
    print()
    print("=" * 40)
    print("       LEADERBOARD")
    print("=" * 40)
    if not scores:
        print("  No scores yet. Play a round!")
    for i, s in enumerate(scores, 1):
        print(f"  {i}. {s['name']} - {s['score']}/{s['total']} ({s['category']}) {s['date']}")
    print()
