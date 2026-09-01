import streamlit as st
from PIL import Image
from datetime import datetime
import random
if "remaining_requests" not in st.session_state:
    st.session_state.remaining_requests = 0
if "remaining_tokens" not in st.session_state:
    st.session_state.remaining_tokens = 0
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
from AH import create_messages, get_response
# --- Page Setup ---
st.set_page_config(
    page_title="A.H",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS Injection
st.markdown("""
<style>
    /* Dark background gradient */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1e222d 0%, #0e1117 100%);
    }

    /* Style Chat Message Containers */
    [data-testid="stChatMessage"] {
        padding: 1rem 1.25rem;
        border-radius: 12px;
        margin-bottom: 0.8rem;
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    /* Distinct styling for Assistant responses */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarCustom"]) {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.7));
        border-left: 3px solid #6366f1;
    }

    /* Input area border highlight */
    .stChatInputContainer {
        border-radius: 14px;
        border: 1px solid rgba(99, 102, 241, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

bg_url =" https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSLGKIE37l8D--a0ONfPweJDsphhGe1s5KCBzJZanTr94U8BQN2VDC_GmQ&s=10"

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(rgba(14, 17, 23, 0.85), rgba(14, 17, 23, 0.95)), 
                url("{bg_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
</style>
""", unsafe_allow_html=True)

st.title("Geopolitical Analyst")
st.caption("Ask questions, analyze geopolitical developments, and explore international policy.")
st.divider()

st.sidebar.subheader("Usage & Remaining Limits")


st.sidebar.metric("Total Tokens Used", f"{st.session_state.total_tokens:,}")


if st.session_state.remaining_requests is not None:

    st.sidebar.metric("Remaining Requests (Today)", f"{st.session_state.remaining_requests:,}")
    
    st.sidebar.metric("Remaining Tokens (Current Window)", f"{st.session_state.remaining_tokens:,}")
else:
    st.sidebar.info("Send your first message to load remaining limits.")

USER_AVATAR = "👤" 
BOT_AVATAR = Image.open("AM.jpg")


current_hour = datetime.now().hour
if current_hour < 12:
    greeting = "Good morning, human."
elif current_hour < 18:
    greeting = "Good afternoon, human."
else:
    greeting = "Good evening, human."
if "messages" not in st.session_state:
    greetings = [
        greeting,
        "Speak, human",
        "How can I assist you today?",
        "I am ready. What are we working on?",
        "Hello! Drop a prompt to get started."

    ]
    st.session_state.messages = [
        {"role": "assistant", "content": random.choice(greetings)}
    ]


for msg in st.session_state.messages:
    avatar = USER_AVATAR if msg["role"] == "user" else BOT_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


if user_prompt := st.chat_input("Type your message here..."):

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(user_prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.spinner("Thinking..."):
   
            bot_reply,used_tokens,rem_toks,rem_req = get_response(user_prompt, st.session_state.messages)
        st.session_state.total_tokens += used_tokens
        st.session_state.remaining_requests += rem_req
        st.session_state.remaining_tokens += rem_toks
        st.markdown(bot_reply)
      

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})