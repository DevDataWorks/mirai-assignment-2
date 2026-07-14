import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=GROQ_API_KEY
)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Multiverse",
    page_icon="🌌",
    layout="centered"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

/* Main App */
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Content */
.main .block-container {
    max-width: 900px;
    padding-top: 2rem;
}

/* Title */
h1 {
    text-align: center;
    color: #60a5fa !important;
}

/* All Text */
p, span, div, label {
    color: #f8fafc !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #111827,
        #1e293b
    );
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background-color: #1e293b;
    color: white;
    border-radius: 12px;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background: #1e293b;
    border-radius: 15px;
    padding: 12px;
    margin-bottom: 12px;
    border: 1px solid #334155;
}

/* Chat Input */
[data-testid="stChatInput"] {
    background-color: #111827;
    border-radius: 15px;
}

[data-testid="stChatInput"] textarea {
    color: white !important;
}

/* Remove white header */
header {
    background: transparent !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );
    color: white;
    border-radius: 10px;
}

/* Hover Effect */
[data-testid="stChatMessage"]:hover {
    border-color: #60a5fa;
    transition: 0.3s;
}

</style>
""", unsafe_allow_html=True)
# -----------------------------
# TITLE
# -----------------------------
st.title("🌌 AI Multiverse")

st.markdown(
    """
    <h3 style='text-align:center;color:#334155;'>
    Chat with Different AI Personalities
    </h3>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("⚙️ App Settings")

personality = st.sidebar.selectbox(
    "Choose a Personality",
    [
        "An Expert Hacker",
        "A Friendly Teacher",
        "A Motivational Speaker",
        "A Panicked College Student at 3 AM",
        "A 1920s Mafia Boss",
        "A Highly Sarcastic Fitness Coach"
    ]
)

intensity = st.sidebar.slider(
    "Intensity Level",
    min_value=1,
    max_value=10,
    value=5
)

# -----------------------------
# DYNAMIC AVATARS
# -----------------------------
if personality == "An Expert Hacker":
    bot_avatar = "💻"

elif personality == "A Friendly Teacher":
    bot_avatar = "📚"

elif personality == "A Motivational Speaker":
    bot_avatar = "🔥"

elif personality == "A Panicked College Student at 3 AM":
    bot_avatar = "😱"

elif personality == "A 1920s Mafia Boss":
    bot_avatar = "🕴️"

elif personality == "A Highly Sarcastic Fitness Coach":
    bot_avatar = "🏋️"

else:
    bot_avatar = "🤖"

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar=message.get("avatar")
    ):
        st.write(message["content"])

# -----------------------------
# CHAT INPUT
# -----------------------------
user_input = st.chat_input("Type your message here...")

if user_input:

    # USER MESSAGE
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # PROMPT ENGINEERING
    ai_instructions = f"""
You are acting as {personality}.

Intensity Level: {intensity}/10

The higher the intensity level, the more strongly you should behave like this personality.

Stay fully in character while answering the user's question.
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": ai_instructions
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        ai_reply = response.choices[0].message.content

        with st.chat_message(
            "assistant",
            avatar=bot_avatar
        ):
            st.write(ai_reply)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": ai_reply,
                "avatar": bot_avatar
            }
        )

    except Exception as e:
        st.error(f"Error: {e}")
