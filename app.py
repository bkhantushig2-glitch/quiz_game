import streamlit as st
import time
from questions import get_categories, get_questions, get_difficulties
from scoring import save_score, get_top_scores, get_player_stats

st.set_page_config(page_title="Quiz Game", page_icon="🧠", layout="centered")

def init_state():
    defaults = {
        "screen": "menu",
        "category": None,
        "difficulty": None,
        "questions": [],
        "current_q": 0,
        "score": 0,
        "q_start_time": None,
        "answers": [],
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def reset_game():
    st.session_state.screen = "menu"
    st.session_state.category = None
    st.session_state.difficulty = None
    st.session_state.questions = []
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.q_start_time = None
    st.session_state.answers = []

def start_quiz(category, difficulty):
    diff = None if difficulty == "All" else difficulty.lower()
    questions = get_questions(category, diff)
    if not questions:
        st.warning("No questions for that difficulty.")
        return
    st.session_state.category = category
    st.session_state.difficulty = difficulty
    st.session_state.questions = questions
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.q_start_time = time.time()
    st.session_state.answers = []
    st.session_state.screen = "quiz"

def submit_answer(picked):
    elapsed = time.time() - st.session_state.q_start_time
    q = st.session_state.questions[st.session_state.current_q]
    correct = picked == q["answer"]
    points = max(1, 10 - int(elapsed)) if correct else 0
    st.session_state.score += points
    st.session_state.answers.append({
        "question": q["question"],
        "picked": picked,
        "answer": q["answer"],
        "correct": correct,
        "points": points,
        "time": round(elapsed, 1),
    })
    st.session_state.current_q += 1
    if st.session_state.current_q >= len(st.session_state.questions):
        st.session_state.screen = "results"
    else:
        st.session_state.q_start_time = time.time()

def show_menu():
    st.title("Quiz Game")
    categories = get_categories()

    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Category", [c.title() for c in categories])
    with col2:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "All"])

    if st.button("Start Quiz", type="primary", use_container_width=True):
        cat_key = category.lower()
        start_quiz(cat_key, difficulty)
        st.rerun()

    st.divider()

    tab1, tab2 = st.tabs(["Leaderboard", "Player Stats"])

    with tab1:
        scores = get_top_scores()
        if not scores:
            st.info("No scores yet. Play a round!")
        else:
            for i, s in enumerate(scores, 1):
                if i == 1:
                    medal = "🥇"
                elif i == 2:
                    medal = "🥈"
                elif i == 3:
                    medal = "🥉"
                else:
                    medal = f"  {i}."
                st.write(f"{medal} **{s['name']}** — {s['score']}/{s['total']} pts ({s['category']}) _{s['date']}_")

    with tab2:
        name = st.text_input("Enter your name to see stats")
        if name:
            stats = get_player_stats(name)
            if not stats:
                st.info("No stats found. Play a round first!")
            else:
                st.write(f"**Games played:** {stats['games']}")
                total = stats["total_questions"]
                correct = stats["total_correct"]
                pct = round(correct / total * 100) if total > 0 else 0
                st.write(f"**Overall:** {correct}/{total} ({pct}%)")
                st.write("**By category:**")
                for cat, data in stats["categories"].items():
                    cat_pct = round(data["correct"] / data["total"] * 100) if data["total"] > 0 else 0
                    st.progress(cat_pct / 100, text=f"{cat.title()}: {data['correct']}/{data['total']} ({cat_pct}%)")

def show_quiz():
    q_index = st.session_state.current_q
    total = len(st.session_state.questions)
    q = st.session_state.questions[q_index]

    st.progress((q_index) / total)
    st.caption(f"Question {q_index + 1} of {total} — {st.session_state.category.title()} ({st.session_state.difficulty})")

    st.subheader(q["question"])

    for option in q["options"]:
        if st.button(option, key=f"opt_{q_index}_{option}", use_container_width=True):
            submit_answer(option)
            st.rerun()

    st.caption("Answer fast for more points! (10 pts max, -1 per second)")

def show_results():
    questions = st.session_state.questions
    max_points = len(questions) * 10
    score = st.session_state.score
    pct = score / max_points * 100 if max_points > 0 else 0

    if pct == 100:
        st.balloons()
        st.title("PERFECT SCORE!")
        st.subheader("You are a champion!")
    elif pct >= 50:
        st.title("Nice job!")
    else:
        st.title("Better luck next time!")

    st.header(f"{score} / {max_points} pts")

    st.divider()
    st.subheader("Answers")
    for a in st.session_state.answers:
        if a["correct"]:
            st.success(f"**{a['question']}** — {a['picked']} (+{a['points']} pts, {a['time']}s)")
        else:
            st.error(f"**{a['question']}** — You picked: {a['picked']} — Answer: {a['answer']} ({a['time']}s)")

    st.divider()
    name = st.text_input("Enter your name for the leaderboard")
    col1, col2 = st.columns(2)
    with col1:
        if name and st.button("Save Score", type="primary"):
            save_score(name, score, max_points, st.session_state.category)
            reset_game()
            st.rerun()
    with col2:
        if st.button("Play Again"):
            reset_game()
            st.rerun()

def main():
    init_state()
    if st.session_state.screen == "menu":
        show_menu()
    elif st.session_state.screen == "quiz":
        show_quiz()
    elif st.session_state.screen == "results":
        show_results()

main()
