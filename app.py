import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Page Config
st.set_page_config(
    page_title="AI Multiverse",
    page_icon="🌌",
    layout="wide"
)

# Personalities
personas = {
    "👨‍🏫 Teacher": "You are a helpful teacher who explains concepts simply.",
    "💻 Software Engineer": "You are an experienced software engineer.",
    "🔥 Motivational Coach": "You motivate users positively.",
    "🚀 Entrepreneur": "You think like a startup founder.",
    "🎓 College Professor": "You explain concepts clearly and academically.",
    "😂 Stand-up Comedian": "You answer in a funny and humorous way."
}

# Sidebar
st.sidebar.title("🌌 AI Multiverse")
st.sidebar.markdown("Choose an AI Personality")

selected_persona = st.sidebar.selectbox(
    "Select Personality",
    list(personas.keys())
)

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Main UI
st.title("🌌 AI Multiverse")
st.write("Talk with different AI personalities from one universe.")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
prompt = st.chat_input("Type your message...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    instruction = personas[selected_persona]

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""
            You are acting as {selected_persona}.

            {instruction}

            User: {prompt}
            """
        )

        answer = response.text

    except Exception:

        if "Teacher" in selected_persona:
            answer = f"""
👨‍🏫 Teacher Mode

That's a great question about "{prompt}".

Let's understand it step by step. Learning becomes easier when complex topics are broken into smaller concepts.
"""

        elif "Software Engineer" in selected_persona:
            answer = f"""
💻 Software Engineer Mode

Regarding "{prompt}", I would approach it using logical thinking, problem-solving, and practical implementation.
"""

        elif "Motivational Coach" in selected_persona:
            answer = f"""
🔥 Motivational Coach Mode

Keep moving forward!

Success in "{prompt}" comes from consistency, effort, and believing in yourself.
"""

        elif "Entrepreneur" in selected_persona:
            answer = f"""
🚀 Entrepreneur Mode

From a business perspective, "{prompt}" could become an opportunity if it solves a real-world problem.
"""

        elif "College Professor" in selected_persona:
            answer = f"""
🎓 College Professor Mode

Academically speaking, "{prompt}" can be analyzed from multiple viewpoints and practical applications.
"""

        else:
            answer = f"""
😂 Stand-up Comedian Mode

You asked about "{prompt}".

I tried debugging life once... turns out the problem was between the keyboard and the chair! 😆
"""

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.write(answer)

st.markdown("---")
st.caption("Built with Streamlit and Gemini AI")