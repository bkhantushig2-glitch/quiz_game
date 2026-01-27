from questions import get_categories, get_questions
from scoring import save_score, get_top_scores
from display import (
    show_welcome, show_menu, show_question,
    show_result, show_final_score, show_leaderboard
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

def play_round(category):
    questions = get_questions(category)
    score = 0

    for i, q in enumerate(questions, 1):
        show_question(i, len(questions), q)
        choice = get_choice("  Your answer: ", len(q["options"]))
        picked = q["options"][choice - 1]
        correct = picked == q["answer"]
        if correct:
            score += 1
        show_result(correct, q["answer"])

    show_final_score(score, len(questions))

    name = input("\nEnter your name for the leaderboard: ").strip()
    if name:
        save_score(name, score, len(questions), category)

def main():
    show_welcome()

    while True:
        categories = get_categories()
        show_menu(categories)

        choice = get_choice("Your choice: ", len(categories) + 2)

        if choice == len(categories) + 2:
            print("Thanks for playing!\n")
            break
        elif choice == len(categories) + 1:
            show_leaderboard(get_top_scores())
        else:
            category = categories[choice - 1]
            play_round(category)

if __name__ == "__main__":
    main()
