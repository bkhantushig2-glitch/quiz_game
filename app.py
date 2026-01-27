import streamlit as st
import time
from questions import get_categories, get_point_values, build_board
from scoring import save_score, get_top_scores

st.set_page_config(page_title="Khantushig's Jeopardy", page_icon="🏆", layout="wide")

POINT_VALUES = get_point_values()

def init_state():
    if "screen" not in st.session_state:
        st.session_state.screen = "start"
    if "players" not in st.session_state:
        st.session_state.players = []
    if "scores" not in st.session_state:
        st.session_state.scores = {}
    if "turn" not in st.session_state:
        st.session_state.turn = 0
    if "board" not in st.session_state:
        st.session_state.board = None
    if "used" not in st.session_state:
        st.session_state.used = set()
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
    if "num_players" not in st.session_state:
        st.session_state.num_players = 2

def new_game():
    st.session_state.board = build_board()
    st.session_state.used = set()
    st.session_state.scores = {p: 0 for p in st.session_state.players}
    st.session_state.turn = 0
    st.session_state.current_q = None
    st.session_state.current_cat = None
    st.session_state.current_pts = 0
    st.session_state.q_start_time = None
    st.session_state.history = []
    st.session_state.screen = "board"

def current_player():
    return st.session_state.players[st.session_state.turn]

def next_turn():
    st.session_state.turn = (st.session_state.turn + 1) % len(st.session_state.players)

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
    player = current_player()

    if correct:
        bonus = max(0, 5 - int(elapsed))
        earned = pts + (bonus * 50)
    else:
        earned = -pts

    st.session_state.scores[player] += earned
    key = f"{st.session_state.current_cat}_{pts}"
    st.session_state.used.add(key)
    st.session_state.history.append({
        "player": player,
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

# ---- SCREENS ----

def show_start():
    st.title("🏆 Khantushig's Jeopardy")
    st.divider()

    num = st.slider("How many players?", min_value=1, max_value=6, value=st.session_state.num_players)
    st.session_state.num_players = num

    names = []
    cols = st.columns(min(num, 3))
    for i in range(num):
        with cols[i % 3]:
            name = st.text_input(f"Player {i + 1}", value=f"Player {i + 1}", key=f"name_{i}")
            names.append(name.strip())

    st.divider()

    with st.expander("Leaderboard"):
        show_leaderboard()

    if st.button("Start Game", type="primary", use_container_width=True):
        st.session_state.players = names
        st.session_state.board = build_board()
        st.session_state.scores = {p: 0 for p in names}
        st.session_state.turn = 0
        st.session_state.used = set()
        st.session_state.history = []
        st.session_state.screen = "board"
        st.rerun()

def show_scoreboard():
    players = st.session_state.players
    scores = st.session_state.scores
    cols = st.columns(len(players))
    for i, player in enumerate(players):
        with cols[i]:
            is_current = (player == current_player() and st.session_state.screen == "board")
            score = scores[player]
            if is_current:
                st.markdown(f"**➤ {player}**")
            else:
                st.markdown(f"**{player}**")
            color = "green" if score >= 0 else "red"
            st.markdown(f":{color}[${score}]")

def show_board():
    st.title("🏆 Khantushig's Jeopardy")
    show_scoreboard()
    st.markdown(f"### {current_player()}'s turn — pick a question!")
    st.divider()

    categories = list(st.session_state.board.keys())
    cols = st.columns(len(categories))

    for col_idx, cat in enumerate(categories):
        with cols[col_idx]:
            st.markdown(f"**{cat.upper()}**")
            for pts in POINT_VALUES:
                key = f"{cat}_{pts}"
                if key in st.session_state.used:
                    st.button("---", key=f"btn_{key}", disabled=True, use_container_width=True)
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
            st.session_state.screen = "start"
            st.rerun()

def show_question():
    q = st.session_state.current_q
    cat = st.session_state.current_cat
    pts = st.session_state.current_pts
    player = current_player()

    show_scoreboard()
    st.divider()
    st.markdown(f"### {player} — {cat.upper()} for ${pts}")
    st.subheader(q["question"])
    st.caption(f"Correct = +${pts} (+ speed bonus) | Wrong = -${pts}")

    for option in q["options"]:
        if st.button(option, key=f"ans_{option}", use_container_width=True):
            answer_question(option)
            st.rerun()

def show_result():
    last = st.session_state.history[-1]

    show_scoreboard()
    st.divider()

    if last["correct"]:
        st.success(f"### {last['player']} got it right! +${last['earned']}")
    else:
        st.error(f"### {last['player']} got it wrong! -${last['max_pts']}")
        st.write(f"The answer was: **{last['answer']}**")

    st.write(f"Time: {last['time']}s")

    if st.button("Next Turn", type="primary", use_container_width=True):
        next_turn()
        st.session_state.screen = "board"
        st.rerun()

def show_final():
    scores = st.session_state.scores
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    winner = ranked[0]

    st.balloons()
    st.title(f"🏆 {winner[0]} wins!")
    st.header(f"Final Score: ${winner[1]}")
    st.divider()

    st.subheader("Final Standings")
    for i, (player, score) in enumerate(ranked, 1):
        if i == 1:
            medal = "🥇"
        elif i == 2:
            medal = "🥈"
        elif i == 3:
            medal = "🥉"
        else:
            medal = f"  {i}."
        color = "green" if score >= 0 else "red"
        st.markdown(f"{medal} **{player}** — :{color}[${score}]")

    st.divider()
    st.subheader("Round Summary")
    for h in st.session_state.history:
        if h["correct"]:
            st.success(f"**{h['player']}** — {h['category'].title()} ${h['max_pts']} — {h['question']} (+${h['earned']}, {h['time']}s)")
        else:
            st.error(f"**{h['player']}** — {h['category'].title()} ${h['max_pts']} — {h['question']} — Answer: {h['answer']} ({h['time']}s)")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save All Scores", type="primary"):
            total = sum(POINT_VALUES) * len(get_categories())
            for player, score in scores.items():
                save_score(player, score, total, "jeopardy")
            st.success("Scores saved!")
    with col2:
        if st.button("Play Again"):
            st.session_state.screen = "start"
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
    if screen == "start":
        show_start()
    elif screen == "board":
        show_board()
    elif screen == "question":
        show_question()
    elif screen == "result":
        show_result()
    elif screen == "final":
        show_final()

main()
