import uuid
import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Cấu hình API
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"

st.set_page_config(page_title="Trợ lý AI", layout="centered")


# ======== Load CSS =========
st.markdown("<style>" + open("static/style.css").read() + "</style>", unsafe_allow_html=True)

# ======== Header =========
st.markdown("<h1 class='title'>🧠 Anh Lập Trình - Trợ Lý AI</h1>", unsafe_allow_html=True)

# Init session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "🤖 Chào sếp! Tôi là Trình, trợ lý AI của bạn. Hãy bắt đầu trò chuyện nhé!"}
    ]

if "input_key" not in st.session_state:
    st.session_state.input_key = str(uuid.uuid4())  # Key input sẽ thay đổi mỗi lần gửi

# === Hiển thị nội dung chat ===
chat_html = '<div class="chat-box">'
for m in st.session_state.messages:
    role, content = m["role"], m["content"]
    if role == "user":
        chat_html += f'<div class="message user">👤 Bạn: {content}</div>'
    elif role == "assistant":
        chat_html += f'<div class="message assistant">🤖: {content}</div>'
    else:
        chat_html += f'<div class="message system">{content}</div>'
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# Inject custom CSS
st.markdown("""
<style>
.chat-container {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
}

.chat-box {
    position: relative;
    width: 100%;
    max-width: 600px;
}

input.custom-input {
    width: 100%;
    padding: 0.75rem 3rem 0.75rem 1rem;
    font-size: 1rem;
    border: 1.5px solid #e63946;
    border-radius: 40px;
    background-color: #1e1e1e;
    color: white;
    outline: none;
}

button.custom-send {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    border: none;
    background: none;
    color: #ccc;
    font-size: 1.5rem;
    cursor: pointer;
}

button.custom-send:hover {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Chat form
with st.form("chat_form", clear_on_submit=True):
    st.markdown('<div class="chat-container"><div class="chat-box">', unsafe_allow_html=True)

    user_input = st.text_input(
        "", placeholder="Các nội dung nhập cần trao đổi ở đây nhé?",
        key="chat_input", label_visibility="collapsed"
    )

    st.markdown('<button type="submit" class="custom-send">➤</button>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)
    submitted = st.form_submit_button("", type="primary")

# Handle submission
if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Đợi Trình trả lời..."):
        try:
            response = openai.ChatCompletion.create(
                model="openai/gpt-3.5-turbo",
                messages=st.session_state.messages,
                max_tokens=150
            )
            reply = response["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"❌ Lỗi: {e}")

    # 💡 Tạo key mới để input trống lần sau
    st.session_state.input_key = str(uuid.uuid4())
    st.rerun()







