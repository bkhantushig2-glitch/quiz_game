import time
from questions import get_categories, get_questions, get_difficulties
from scoring import save_score, get_top_scores, get_player_stats
from display import (
    show_welcome, show_menu, show_question,
    show_result, show_final_score, show_leaderboard,
    show_difficulty_menu, show_player_stats
)

def get_choice(prompt, max_val):
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= max_val:
                return choice
            print(f"  Pick a number between 1 and {max_val}")
        except ValueError:
            print("  Enter a number")

def pick_difficulty():
    show_difficulty_menu()
    choice = get_choice("Your choice: ", 4)
    difficulties = get_difficulties()
    if choice == 4:
        return None
    return difficulties[choice - 1]

def play_round(category):
    difficulty = pick_difficulty()
    questions = get_questions(category, difficulty)

    if not questions:
        print("  No questions for that difficulty. Try another!")
        return

    score = 0
    max_points = len(questions) * 10

    for i, q in enumerate(questions, 1):
        show_question(i, len(questions), q)
        start = time.time()
        choice = get_choice("  Your answer: ", len(q["options"]))
        elapsed = time.time() - start
        picked = q["options"][choice - 1]
        correct = picked == q["answer"]
        points = max(1, 10 - int(elapsed)) if correct else 0
        score += points
        show_result(correct, q["answer"], elapsed, points)

    show_final_score(score, max_points)

    name = input("\nEnter your name for the leaderboard: ").strip()
    if name:
        save_score(name, score, max_points, category)

def main():
    show_welcome()

    while True:
        categories = get_categories()
        show_menu(categories)

        choice = get_choice("Your choice: ", len(categories) + 3)

        if choice == len(categories) + 3:
            print("Thanks for playing!\n")
            break
        elif choice == len(categories) + 1:
            show_leaderboard(get_top_scores())
        elif choice == len(categories) + 2:
            name = input("Enter your name: ").strip()
            if name:
                stats = get_player_stats(name)
                show_player_stats(name, stats)
        else:
            category = categories[choice - 1]
            play_round(category)

if __name__ == "__main__":
    main()
