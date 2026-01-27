import streamlit as st
import time
from questions import get_categories, get_point_values, build_board
from scoring import save_score, get_top_scores, get_player_stats

st.set_page_config(page_title="Khantushig's Jeopardy", page_icon="🏆", layout="wide")

POINT_VALUES = get_point_values()

def init_state():
    if "screen" not in st.session_state:
        st.session_state.screen = "board"
    if "board" not in st.session_state:
        st.session_state.board = build_board()
    if "used" not in st.session_state:
        st.session_state.used = set()
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "current_q" not in st.session_state:
        st.session_state.current_q = None
    if "current_cat" not in st.session_state:
        st.session_state.current_cat = None
    if "current_pts" not in st.session_state:
        st.session_state.current_pts = 0
    if "q_start_time" not in st.session_state:
        st.session_state.q_start_time = None
    if "history" not in st.session_state:
        st.session_state.history = []
    if "max_possible" not in st.session_state:
        st.session_state.max_possible = sum(POINT_VALUES) * len(get_categories())

def new_game():
    st.session_state.board = build_board()
    st.session_state.used = set()
    st.session_state.score = 0
    st.session_state.current_q = None
    st.session_state.current_cat = None
    st.session_state.current_pts = 0
    st.session_state.q_start_time = None
    st.session_state.history = []
    st.session_state.screen = "board"

def pick_question(cat, pts):
    st.session_state.current_q = st.session_state.board[cat][pts]
    st.session_state.current_cat = cat
    st.session_state.current_pts = pts
    st.session_state.q_start_time = time.time()
    st.session_state.screen = "question"

def answer_question(picked):
    q = st.session_state.current_q
    elapsed = time.time() - st.session_state.q_start_time
    correct = picked == q["answer"]
    pts = st.session_state.current_pts

    if correct:
        bonus = max(0, 5 - int(elapsed))
        earned = pts + (bonus * 50)
    else:
        earned = 0

    st.session_state.score += earned
    key = f"{st.session_state.current_cat}_{pts}"
    st.session_state.used.add(key)
    st.session_state.history.append({
        "category": st.session_state.current_cat,
        "question": q["question"],
        "picked": picked,
        "answer": q["answer"],
        "correct": correct,
        "earned": earned,
        "max_pts": pts,
        "time": round(elapsed, 1),
    })

    total_cells = len(get_categories()) * len(POINT_VALUES)
    if len(st.session_state.used) >= total_cells:
        st.session_state.screen = "final"
    else:
        st.session_state.screen = "result"

def show_board():
    st.title("🏆 Khantushig's Jeopardy")
    st.markdown(f"**Score: {st.session_state.score}**")

    categories = list(st.session_state.board.keys())
    cols = st.columns(len(categories))

    for col_idx, cat in enumerate(categories):
        with cols[col_idx]:
            st.markdown(f"**{cat.upper()}**")
            for pts in POINT_VALUES:
                key = f"{cat}_{pts}"
                if key in st.session_state.used:
                    st.button(f"---", key=f"btn_{key}", disabled=True, use_container_width=True)
                else:
                    if st.button(f"${pts}", key=f"btn_{key}", use_container_width=True):
                        pick_question(cat, pts)
                        st.rerun()

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Finish Game"):
            st.session_state.screen = "final"
            st.rerun()
    with col2:
        if st.button("New Game"):
            new_game()
            st.rerun()

    with st.expander("Leaderboard"):
        show_leaderboard()

def show_question():
    q = st.session_state.current_q
    cat = st.session_state.current_cat
    pts = st.session_state.current_pts

    st.markdown(f"### {cat.upper()} for ${pts}")
    st.divider()
    st.subheader(q["question"])
    st.caption("Answer fast for bonus points!")

    for option in q["options"]:
        if st.button(option, key=f"ans_{option}", use_container_width=True):
            answer_question(option)
            st.rerun()

def show_result():
    last = st.session_state.history[-1]

    if last["correct"]:
        st.success(f"### Correct! +${last['earned']}")
    else:
        st.error(f"### Wrong! The answer was: {last['answer']}")

    st.write(f"Time: {last['time']}s")
    st.write(f"**Current score: ${st.session_state.score}**")

    if st.button("Back to Board", type="primary", use_container_width=True):
        st.session_state.screen = "board"
        st.rerun()

def show_final():
    score = st.session_state.score
    total = st.session_state.max_possible

    if score >= total * 0.8:
        st.balloons()
        st.title("🏆 AMAZING!")
    elif score >= total * 0.5:
        st.title("👏 Nice job!")
    else:
        st.title("Game Over!")

    st.header(f"Final Score: ${score}")

    correct_count = sum(1 for h in st.session_state.history if h["correct"])
    total_answered = len(st.session_state.history)
    st.write(f"**{correct_count}/{total_answered}** questions correct")

    st.divider()
    st.subheader("Round Summary")
    for h in st.session_state.history:
        if h["correct"]:
            st.success(f"**{h['category'].title()} ${h['max_pts']}** — {h['question']} (+${h['earned']}, {h['time']}s)")
        else:
            st.error(f"**{h['category'].title()} ${h['max_pts']}** — {h['question']} — Answer: {h['answer']} ({h['time']}s)")

    st.divider()
    name = st.text_input("Enter your name for the leaderboard")
    col1, col2 = st.columns(2)
    with col1:
        if name and st.button("Save Score", type="primary"):
            save_score(name, score, total, "jeopardy")
            new_game()
            st.rerun()
    with col2:
        if st.button("Play Again"):
            new_game()
            st.rerun()

def show_leaderboard():
    scores = get_top_scores(10)
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
            st.write(f"{medal} **{s['name']}** — {s['score']}/{s['total']} pts _{s['date']}_")

def main():
    init_state()
    screen = st.session_state.screen
    if screen == "board":
        show_board()
    elif screen == "question":
        show_question()
    elif screen == "result":
        show_result()
    elif screen == "final":
        show_final()

main()
