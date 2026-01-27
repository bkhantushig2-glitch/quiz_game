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
    print(f"\nQuestion {num}/{total}  {YELLOW}(answer fast for more points!){RESET}")
    print(f"  {q['question']}")
    for i, option in enumerate(q["options"], 1):
        print(f"    {i}. {option}")

def show_result(correct, answer, elapsed, points):
    secs = f"{elapsed:.1f}s"
    if correct:
        print(f"  {GREEN}Correct!{RESET} ({secs}) {BOLD}+{points} pts{RESET}")
    else:
        print(f"  {RED}Wrong!{RESET} The answer was: {YELLOW}{answer}{RESET} ({secs}) +0 pts")

def show_final_score(score, total):
    print()
    print("-" * 30)
    print(f"  You scored {BOLD}{score}/{total} pts{RESET}")
    pct = score / total * 100 if total > 0 else 0
    if pct == 100:
        print()
        print(f"  {YELLOW}*   *   *   *   *   *   *{RESET}")
        print(f"  {GREEN}    PERFECT SCORE!{RESET}")
        print(f"  {YELLOW}*   *   *   *   *   *   *{RESET}")
        print()
        print(f"  {GREEN}    You are a champion!{RESET}")
    elif pct >= 50:
        print(f"  {GREEN}Nice job!{RESET}")
    else:
        print(f"  {RED}Better luck next time!{RESET}")
    print("-" * 30)

def _pad_name(name, width=10):
    if len(name) > width:
        return name[:width]
    return name.center(width)

def show_podium(scores):
    if len(scores) < 3:
        return

    first = _pad_name(scores[0]["name"])
    second = _pad_name(scores[1]["name"])
    third = _pad_name(scores[2]["name"])
    s1 = f"{scores[0]['score']}/{scores[0]['total']}"
    s2 = f"{scores[1]['score']}/{scores[1]['total']}"
    s3 = f"{scores[2]['score']}/{scores[2]['total']}"

    print(f"              {YELLOW}** 1ST **{RESET}")
    print(f"              {YELLOW}{first}{RESET}")
    print(f"              {YELLOW}  {s1}  {RESET}")
    print(f"            ___________")
    print(f"           |           |")
    print(f"  {second}|           |{third}")
    print(f"    {s2}  |           |  {s3}")
    print(f"  _________|           |_________")
    print(f" | 2ND     |    1ST    |     3RD |")
    print(f" |_________|___________|_________|")
    print()

def show_leaderboard(scores):
    print()
    print("=" * 40)
    print(f"       {BOLD}LEADERBOARD{RESET}")
    print("=" * 40)

    if not scores:
        print("  No scores yet. Play a round!")
        print()
        return

    show_podium(scores)

    for i, s in enumerate(scores, 1):
        if i == 1:
            color = YELLOW
        elif i == 2:
            color = GREEN
        else:
            color = RESET
        print(f"  {color}{i}. {s['name']} - {s['score']}/{s['total']} ({s['category']}) {s['date']}{RESET}")
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
