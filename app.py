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
try:
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

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

custom_css = """
<style>
/* Form container */
.chat-form {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
}

/* Custom input field */
.custom-input {
    flex: 1;
    padding: 0.6rem 1rem;
    font-size: 1rem;
    border: 1.5px solid #e63946;
    background-color: #1e1e1e;
    color: white;
    border-radius: 50px;
    outline: none;
}

/* Send button styled as icon */
.custom-send-btn {
    margin-left: -50px;
    background: none;
    border: none;
    color: #ccc;
    font-size: 1.5rem;
    cursor: pointer;
}

.custom-send-btn:hover {
    color: white;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# === Input & xử lý gửi ===
with st.form("chat_input", clear_on_submit=True):
    st.markdown('<div class="chat-form">', unsafe_allow_html=True)
    
    # Ô nhập input
    user_input = st.text_input(
        label="",
        placeholder="Các nội dung nhập cần trao đổi ở đây nhé?",
        key="custom_input",
        label_visibility="collapsed"
    )

    # Icon nút gửi ➤
    st.markdown('<button class="custom-send-btn" type="submit">➤</button>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    submitted = st.form_submit_button("", type="primary")

# === Xử lý khi gửi ===
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







