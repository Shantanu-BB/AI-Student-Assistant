"""
AI Student Assistant
A beginner-friendly AI tutor chatbot built with Streamlit and Google Gemini.
"""

import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

load_dotenv()

APP_TITLE = "AI Student Assistant"
APP_SUBTITLE = "Learn Artificial Intelligence through conversation"

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

SYSTEM_PROMPT = """
You are "AI Student Assistant", a friendly and patient AI tutor for beginners.

Your teaching style:
- Explain concepts in simple, everyday language.
- Give a short, relatable example whenever useful.
- Avoid unnecessarily complicated terminology.
- If you use a technical term, explain it immediately in simple words.
- Keep answers clear and well organized.
- Use bullet points when useful.
- Help students understand concepts instead of just giving definitions.
- Be encouraging and beginner-friendly.

Scope:
- You mainly help students learn Artificial Intelligence,
  Machine Learning, Python, Data Science, SQL, and related technology.
- You can also help with general study questions.
- For unrelated harmless questions, answer briefly and remind the student
  that you are mainly designed as a student learning assistant.
""".strip()

EXAMPLE_PROMPTS = [
    "What is Artificial Intelligence?",
    "What is Machine Learning?",
    "What is SQL?",
    "Explain supervised and unsupervised learning.",
]

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="centered",
)

# -----------------------------
# Styling
# -----------------------------

st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 0;
            background: linear-gradient(90deg, #4F46E5, #06B6D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            color: #6B7280;
            font-size: 1.05rem;
            margin-top: 0.2rem;
            margin-bottom: 1.5rem;
        }

        .stButton > button {
            width: 100%;
            border-radius: 12px;
        }

        @media (max-width: 640px) {
            .main-title {
                font-size: 1.7rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Gemini Client
# -----------------------------

def get_client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key or api_key == "your_api_key_here":
        return None

    return genai.Client(api_key=api_key)


# -----------------------------
# Convert messages
# -----------------------------

def build_contents(messages):
    contents = []

    for message in messages:
        role = "user" if message["role"] == "user" else "model"

        contents.append(
            types.Content(
                role=role,
                parts=[
                    types.Part.from_text(
                        text=message["content"]
                    )
                ],
            )
        )

    return contents


# -----------------------------
# Streaming AI response
# -----------------------------

def stream_ai_response(client, messages):
    contents = build_contents(messages)

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,

        # Lower output length helps the chatbot respond faster.
        max_output_tokens=600,

        # Balanced creativity and consistency.
        temperature=0.5,
    )

    response_stream = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=contents,
        config=config,
    )

    for chunk in response_stream:
        text = getattr(chunk, "text", None)

        if text:
            yield text


# -----------------------------
# Error messages
# -----------------------------

def friendly_error(error):
    text = str(error).lower()

    if (
        "api key" in text
        or "api_key" in text
        or "permission" in text
        or "401" in text
        or "403" in text
    ):
        return (
            "🔑 Your API key looks invalid. "
            "Please check the GEMINI_API_KEY in your `.env` file."
        )

    if "429" in text or "quota" in text or "rate" in text:
        return (
            "⏳ Too many requests or the free quota is temporarily used up. "
            "Please wait a moment and try again."
        )

    if "503" in text or "unavailable" in text:
        return (
            "⚡ The Gemini model is temporarily busy because of high demand. "
            "Please try again after a few seconds."
        )

    if "404" in text or "not found" in text:
        return (
            f"❌ The model `{MODEL_NAME}` was not found. "
            "Please check GEMINI_MODEL in your `.env` file."
        )

    if "connect" in text or "network" in text or "timeout" in text:
        return (
            "🌐 Network problem. "
            "Please check your internet connection and try again."
        )

    return f"Something went wrong while contacting the AI: {error}"


# -----------------------------
# Chat controls
# -----------------------------

def clear_chat():
    st.session_state.messages = []
    st.session_state.pending_prompt = None


def set_prompt(prompt):
    st.session_state.pending_prompt = prompt


if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.header("🎓 " + APP_TITLE)

    st.subheader("About the Project")

    st.write(
        "A beginner-friendly chatbot that works as an AI tutor. "
        "Ask questions about Artificial Intelligence, Machine Learning, "
        "Python, SQL and technology."
    )

    st.subheader("Technologies Used")

    st.markdown(
        "- 🐍 Python\n"
        "- 🎈 Streamlit\n"
        "- ✨ Google Gemini API\n"
        "- 🔐 python-dotenv\n"
        "- ⚡ Streaming responses"
    )

    st.divider()

    st.button(
        "🗑️ Clear Chat",
        on_click=clear_chat,
        use_container_width=True,
    )


# -----------------------------
# Main UI
# -----------------------------

st.markdown(
    f'<p class="main-title">🎓 {APP_TITLE}</p>',
    unsafe_allow_html=True,
)

st.markdown(
    f'<p class="subtitle">{APP_SUBTITLE}</p>',
    unsafe_allow_html=True,
)


# -----------------------------
# API Client
# -----------------------------

client = get_client()

if client is None:
    st.error(
        "**Gemini API key not found.**\n\n"
        "1. Create a `.env` file.\n"
        "2. Add your Gemini API key.\n"
        "3. Save the file.\n"
        "4. Restart the app."
    )

    st.stop()


# -----------------------------
# Display previous messages
# -----------------------------

for message in st.session_state.messages:

    avatar = (
        "🧑‍🎓"
        if message["role"] == "user"
        else "🤖"
    )

    with st.chat_message(
        message["role"],
        avatar=avatar,
    ):
        st.markdown(message["content"])


# -----------------------------
# Example prompts
# -----------------------------

if (
    not st.session_state.messages
    and not st.session_state.pending_prompt
):
    st.markdown("#### 💡 Try asking:")

    col1, col2 = st.columns(2)

    for i, example in enumerate(EXAMPLE_PROMPTS):

        with col1 if i % 2 == 0 else col2:

            st.button(
                example,
                key=f"example_{i}",
                on_click=set_prompt,
                args=(example,),
            )


# -----------------------------
# User input
# -----------------------------

typed_prompt = st.chat_input(
    "Ask me anything about AI..."
)

prompt = (
    st.session_state.pending_prompt
    or typed_prompt
)

st.session_state.pending_prompt = None


# -----------------------------
# Generate answer
# -----------------------------

if prompt:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message(
        "user",
        avatar="🧑‍🎓",
    ):
        st.markdown(prompt)


    # Show streaming assistant response
    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        try:

            response_placeholder = st.empty()

            full_response = ""

            with st.spinner("Thinking..."):

                for chunk in stream_ai_response(
                    client,
                    st.session_state.messages,
                ):

                    full_response += chunk

                    # Show text immediately as it arrives
                    response_placeholder.markdown(
                        full_response + "▌"
                    )

            # Remove cursor after completion
            response_placeholder.markdown(
                full_response
            )

            # Save complete answer
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response,
                }
            )

        except Exception as e:

            st.error(
                friendly_error(e)
            )
