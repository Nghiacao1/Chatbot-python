import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Cấu hình API
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"

st.set_page_config(page_title="Trợ lý AI", layout="centered")

# Load CSS custom
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='title'>🧠 Anh Lập Trình - Trợ Lý AI</h1>", unsafe_allow_html=True)

# Lưu lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "🤖 Chào sếp! Tôi là Trình, trợ lý AI của bạn. Hãy bắt đầu trò chuyện nhé!"}
    ]

# Hiển thị lịch sử
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

# ======== RESET TRƯỚC KHI RENDER WIDGET =========
if "reset_input" in st.session_state and st.session_state.reset_input:
    del st.session_state["temp_input"]
    st.session_state.reset_input = False
    st.rerun()

# ======== KHỞI TẠO BAN ĐẦU =========
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "🤖 Chào sếp! Tôi là Trình, trợ lý AI của bạn. Hãy bắt đầu trò chuyện nhé!"}
    ]

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

# ======== INPUT BOX =========
user_input = st.text_input("Sếp nhập nội dung cần trao đổi ở đây nhé?",
                           placeholder="Nhập nội dung...",
                           label_visibility="collapsed",
                           key="temp_input")

# ======== XỬ LÝ GỬI =========
if user_input and user_input != st.session_state.last_input:
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

            # Đánh dấu đã gửi input này
            st.session_state.last_input = user_input

            # Đặt cờ reset input
            st.session_state.reset_input = True
            st.rerun()

        except Exception as e:
            st.error(f"❌ Lỗi: {e}")






