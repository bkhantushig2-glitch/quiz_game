GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

def show_welcome():
    print()
    print("=" * 40)
    print(f"        {BOLD}QUIZ GAME{RESET}")
    print("=" * 40)
    print()

def show_menu(categories):
    print("Pick a category:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat.title()}")
    print(f"  {len(categories) + 1}. Leaderboard")
    print(f"  {len(categories) + 2}. Player Stats")
    print(f"  {len(categories) + 3}. Quit")
    print()

def show_difficulty_menu():
    print("\nPick a difficulty:")
    print("  1. Easy")
    print("  2. Medium")
    print("  3. Hard")
    print("  4. All")
    print()

def show_question(num, total, q):
    print(f"\nQuestion {num}/{total}")
    print(f"  {q['question']}")
    for i, option in enumerate(q["options"], 1):
        print(f"    {i}. {option}")

def show_result(correct, answer):
    if correct:
        print(f"  {GREEN}Correct!{RESET}")
    else:
        print(f"  {RED}Wrong!{RESET} The answer was: {YELLOW}{answer}{RESET}")

def show_final_score(score, total):
    print()
    print("-" * 30)
    print(f"  You got {BOLD}{score}/{total}{RESET}")
    if score == total:
        print(f"  {GREEN}Perfect score!{RESET}")
    elif score >= total / 2:
        print(f"  {GREEN}Nice job!{RESET}")
    else:
        print(f"  {RED}Better luck next time!{RESET}")
    print("-" * 30)

def show_leaderboard(scores):
    print()
    print("=" * 40)
    print(f"       {BOLD}LEADERBOARD{RESET}")
    print("=" * 40)
    if not scores:
        print("  No scores yet. Play a round!")
    for i, s in enumerate(scores, 1):
        print(f"  {i}. {s['name']} - {s['score']}/{s['total']} ({s['category']}) {s['date']}")
    print()

def show_player_stats(name, stats):
    print()
    print("=" * 40)
    print(f"       {BOLD}STATS FOR {name.upper()}{RESET}")
    print("=" * 40)

    if not stats:
        print("  No stats found. Play a round first!")
        print()
        return

    print(f"  Games played: {stats['games']}")
    total = stats['total_questions']
    correct = stats['total_correct']
    pct = round(correct / total * 100) if total > 0 else 0
    print(f"  Overall: {correct}/{total} ({pct}%)")
    print()

    print(f"  {BOLD}By category:{RESET}")
    for cat, data in stats["categories"].items():
        cat_pct = round(data['correct'] / data['total'] * 100) if data['total'] > 0 else 0
        color = GREEN if cat_pct >= 50 else RED
        print(f"    {cat.title():12s} {color}{data['correct']}/{data['total']} ({cat_pct}%){RESET}")
    print()
