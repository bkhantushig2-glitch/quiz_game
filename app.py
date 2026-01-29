import streamlit as st
import time
import os
from questions import get_categories, get_point_values, build_board
from scoring import save_score, get_top_scores, SCORES_FILE

st.set_page_config(page_title="Khantushig's Jeopardy", page_icon="🎯", layout="wide")

# Custom CSS for Gen Z vibes
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #ffffff;
        font-size: 1.2rem;
        margin-top: 0;
    }
    /* Make all text white for visibility */
    .stMarkdown, .stText, p, span, label, .stSelectbox label, .stTextInput label {
        color: #ffffff !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    .stExpander p, .stExpander span {
        color: #ffffff !important;
    }
    .player-card {
        background: linear-gradient(145deg, #2d2d44, #1a1a2e);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 2px solid #3d3d5c;
        transition: all 0.3s ease;
    }
    .player-card:hover {
        transform: translateY(-5px);
        border-color: #ff6b6b;
    }
    .score-positive {
        color: #2ecc71;
        font-size: 2rem;
        font-weight: bold;
    }
    .score-negative {
        color: #e74c3c;
        font-size: 2rem;
        font-weight: bold;
    }
    .question-box {
        background: linear-gradient(145deg, #2d2d44, #1a1a2e);
        border-radius: 20px;
        padding: 30px;
        border: 3px solid #48dbfb;
        margin: 20px 0;
    }
    .category-header {
        color: #feca57;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    div[data-testid="stButton"] button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    div[data-testid="stButton"] button:hover {
        transform: scale(1.02);
    }
    /* Fix caption and other muted text */
    .stCaption, small, .st-emotion-cache-1gulkj5 {
        color: #e0e0e0 !important;
    }
    /* Fix selectbox and input text */
    .stSelectbox > div > div, .stTextInput > div > div > input {
        color: #ffffff !important;
        background-color: #2d2d44 !important;
    }
    /* Fix expander text */
    .streamlit-expanderHeader {
        color: #ffffff !important;
    }
    /* Fix info/success/error box text */
    .stAlert p {
        color: #1a1a2e !important;
    }
</style>
""", unsafe_allow_html=True)

POINT_VALUES = get_point_values()

def init_state():
    defaults = {
        "screen": "start",
        "players": [],
        "scores": {},
        "board": None,
        "used": set(),
        "current_q": None,
        "current_cat": None,
        "current_pts": 0,
        "history": [],
        "num_players": 2,
        "show_answer": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def clear_all_scores():
    if os.path.exists(SCORES_FILE):
        os.remove(SCORES_FILE)

def reset_to_start():
    st.session_state.screen = "start"
    st.session_state.players = []
    st.session_state.scores = {}
    st.session_state.board = None
    st.session_state.used = set()
    st.session_state.current_q = None
    st.session_state.history = []
    st.session_state.show_answer = False

def pick_question(cat, pts):
    st.session_state.current_q = st.session_state.board[cat][pts]
    st.session_state.current_cat = cat
    st.session_state.current_pts = pts
    st.session_state.show_answer = False
    st.session_state.screen = "question"

def award_points(player, correct):
    pts = st.session_state.current_pts
    cat = st.session_state.current_cat
    q = st.session_state.current_q

    if correct:
        st.session_state.scores[player] += pts
        earned = pts
    else:
        st.session_state.scores[player] -= pts
        earned = -pts

    key = f"{cat}_{pts}"
    st.session_state.used.add(key)
    st.session_state.history.append({
        "player": player,
        "category": cat,
        "question": q["question"],
        "answer": q["answer"],
        "correct": correct,
        "earned": earned,
    })

    total_cells = len(get_categories()) * len(POINT_VALUES)
    if len(st.session_state.used) >= total_cells:
        st.session_state.screen = "final"
    else:
        st.session_state.screen = "board"

def skip_question():
    key = f"{st.session_state.current_cat}_{st.session_state.current_pts}"
    st.session_state.used.add(key)
    st.session_state.history.append({
        "player": "Nobody",
        "category": st.session_state.current_cat,
        "question": st.session_state.current_q["question"],
        "answer": st.session_state.current_q["answer"],
        "correct": False,
        "earned": 0,
    })
    total_cells = len(get_categories()) * len(POINT_VALUES)
    if len(st.session_state.used) >= total_cells:
        st.session_state.screen = "final"
    else:
        st.session_state.screen = "board"

# ---- SCREENS ----

def show_start():
    st.markdown('<h1 class="main-title">🎯 JEOPARDY</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">by Khantushig Batbold</p>', unsafe_allow_html=True)
    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 👥 How many players?")
        num = st.selectbox(
            "Players",
            options=[1, 2, 3, 4, 5, 6],
            index=1,
            label_visibility="collapsed"
        )
        st.session_state.num_players = num

        st.write("")
        st.markdown("### ✏️ Enter names")
        names = []
        for i in range(num):
            name = st.text_input(
                f"Player {i + 1}",
                value=f"Player {i + 1}",
                key=f"name_{i}",
                label_visibility="collapsed",
                placeholder=f"Player {i + 1} name..."
            )
            names.append(name.strip() if name.strip() else f"Player {i + 1}")

        st.write("")
        st.write("")

        if st.button("🚀 START GAME", type="primary", use_container_width=True):
            st.session_state.players = names
            st.session_state.board = build_board()
            st.session_state.scores = {p: 0 for p in names}
            st.session_state.used = set()
            st.session_state.history = []
            st.session_state.screen = "board"
            st.rerun()

        st.write("")
        st.divider()

        col_a, col_b = st.columns(2)
        with col_a:
            with st.expander("🏆 Leaderboard"):
                show_leaderboard()
        with col_b:
            if st.button("🗑️ Clear All Scores", use_container_width=True):
                clear_all_scores()
                st.success("All scores cleared! 🧹")
                st.rerun()

def show_scoreboard():
    players = st.session_state.players
    scores = st.session_state.scores
    cols = st.columns(len(players))

    for i, player in enumerate(players):
        with cols[i]:
            score = scores[player]
            emoji = "🔥" if score > 0 else "💀" if score < 0 else "😐"
            color_class = "score-positive" if score >= 0 else "score-negative"
            st.markdown(f"""
                <div style="text-align: center; padding: 10px; background: linear-gradient(145deg, #2d2d44, #1a1a2e); border-radius: 12px; border: 2px solid {'#2ecc71' if score >= 0 else '#e74c3c'};">
                    <div style="font-size: 1.1rem; color: #fff; margin-bottom: 5px;">{emoji} {player}</div>
                    <div class="{color_class}">${score}</div>
                </div>
            """, unsafe_allow_html=True)

def show_board():
    st.markdown('<h1 class="main-title">🎯 JEOPARDY</h1>', unsafe_allow_html=True)
    st.write("")
    show_scoreboard()
    st.write("")
    st.divider()

    categories = list(st.session_state.board.keys())
    cols = st.columns(len(categories))

    for col_idx, cat in enumerate(categories):
        with cols[col_idx]:
            st.markdown(f'<p class="category-header">{cat.upper()}</p>', unsafe_allow_html=True)
            for pts in POINT_VALUES:
                key = f"{cat}_{pts}"
                if key in st.session_state.used:
                    st.button("✓", key=f"btn_{key}", disabled=True, use_container_width=True)
                else:
                    if st.button(f"${pts}", key=f"btn_{key}", use_container_width=True):
                        pick_question(cat, pts)
                        st.rerun()

    st.write("")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏁 End Game", use_container_width=True):
            st.session_state.screen = "final"
            st.rerun()
    with col2:
        if st.button("🔄 New Game", use_container_width=True):
            reset_to_start()
            st.rerun()

def show_question():
    q = st.session_state.current_q
    cat = st.session_state.current_cat
    pts = st.session_state.current_pts

    st.markdown('<h1 class="main-title">🎯 JEOPARDY</h1>', unsafe_allow_html=True)
    st.write("")
    show_scoreboard()
    st.write("")

    st.markdown(f"""
        <div class="question-box">
            <p class="category-header">{cat.upper()} — ${pts}</p>
            <h2 style="color: #fff; text-align: center; margin: 20px 0;">{q['question']}</h2>
        </div>
    """, unsafe_allow_html=True)

    # Show/hide answer toggle
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("👁️ Show Answer" if not st.session_state.show_answer else "🙈 Hide Answer", use_container_width=True):
            st.session_state.show_answer = not st.session_state.show_answer
            st.rerun()

        if st.session_state.show_answer:
            st.success(f"**Answer:** {q['answer']}")

    st.write("")
    st.divider()
    st.markdown("### 🎉 Who got it right?")
    st.caption("Click the player who answered correctly, or mark wrong/skip")

    # Player buttons
    players = st.session_state.players
    cols = st.columns(len(players))
    for i, player in enumerate(players):
        with cols[i]:
            if st.button(f"✅ {player}", key=f"correct_{player}", use_container_width=True):
                award_points(player, True)
                st.rerun()

    st.write("")
    st.markdown("### ❌ Who got it wrong?")
    cols2 = st.columns(len(players))
    for i, player in enumerate(players):
        with cols2[i]:
            if st.button(f"❌ {player}", key=f"wrong_{player}", use_container_width=True, type="secondary"):
                award_points(player, False)
                st.rerun()

    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⏭️ Skip (nobody answered)", use_container_width=True):
            skip_question()
            st.rerun()

def show_final():
    scores = st.session_state.scores
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    winner = ranked[0]

    st.balloons()
    st.markdown('<h1 class="main-title">🏆 GAME OVER</h1>', unsafe_allow_html=True)
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div style="text-align: center; padding: 30px; background: linear-gradient(145deg, #2d2d44, #1a1a2e); border-radius: 20px; border: 3px solid #feca57;">
                <div style="font-size: 4rem;">👑</div>
                <div style="font-size: 2rem; color: #feca57; font-weight: bold;">{winner[0]}</div>
                <div style="font-size: 3rem; color: #2ecc71; font-weight: bold;">${winner[1]}</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.divider()
    st.markdown("### 📊 Final Standings")

    for i, (player, score) in enumerate(ranked, 1):
        if i == 1:
            medal = "🥇"
        elif i == 2:
            medal = "🥈"
        elif i == 3:
            medal = "🥉"
        else:
            medal = f"#{i}"
        color = "#2ecc71" if score >= 0 else "#e74c3c"
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; margin: 5px 0; background: linear-gradient(145deg, #2d2d44, #1a1a2e); border-radius: 10px;">
                <span style="font-size: 1.3rem;">{medal} {player}</span>
                <span style="font-size: 1.3rem; color: {color}; font-weight: bold;">${score}</span>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.divider()

    with st.expander("📜 Round History"):
        for h in st.session_state.history:
            if h["player"] == "Nobody":
                st.info(f"⏭️ **{h['category'].title()} ${abs(h['earned']) if h['earned'] != 0 else st.session_state.current_pts}** — Skipped")
            elif h["correct"]:
                st.success(f"✅ **{h['player']}** — {h['category'].title()} +${h['earned']}")
            else:
                st.error(f"❌ **{h['player']}** — {h['category'].title()} -${abs(h['earned'])}")

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Scores", type="primary", use_container_width=True):
            total = sum(POINT_VALUES) * len(get_categories())
            for player, score in scores.items():
                save_score(player, score, total, "jeopardy")
            st.success("Scores saved! 🎉")
    with col2:
        if st.button("🔄 Play Again", use_container_width=True):
            reset_to_start()
            st.rerun()

def show_leaderboard():
    scores = get_top_scores(10)
    if not scores:
        st.info("No scores yet! Play a game 🎮")
    else:
        for i, s in enumerate(scores, 1):
            if i == 1:
                medal = "🥇"
            elif i == 2:
                medal = "🥈"
            elif i == 3:
                medal = "🥉"
            else:
                medal = f"#{i}"
            st.write(f"{medal} **{s['name']}** — ${s['score']}")

def main():
    init_state()
    screen = st.session_state.screen
    if screen == "start":
        show_start()
    elif screen == "board":
        show_board()
    elif screen == "question":
        show_question()
    elif screen == "final":
        show_final()

main()
