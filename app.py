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

# Khởi tạo biến tạm nếu chưa có
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "temp_input" not in st.session_state:
    st.session_state.temp_input = ""

# Ô nhập liệu
user_input = st.text_input("Sếp nhập nội dung cần trao đổi ở đây nhé?",
                           placeholder="Nhập nội dung...",
                           label_visibility="collapsed",
                           key="temp_input")

# Nếu có input mới và khác với lần trước
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

            # Cập nhật input cuối cùng để tránh gửi lại
            st.session_state.last_input = user_input

            # Reset input bằng cách gán rỗng key temp_input rồi rerun
            st.session_state.temp_input = ""
            st.experimental_rerun()

        except Exception as e:
            st.error(f"❌ Lỗi: {e}")





