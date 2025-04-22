import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Config
openai.api_key = os.getenv("OPENROUTER_API_KEY")

if openai.api_key is None:
    raise ValueError("Không thể tìm thấy API Key trong .env!")
# Set page config
st.set_page_config(page_title="Trợ lý AI", layout="centered")

# Load CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='title'>🧠 Anh Lập Trình - Trợ Lý AI</h1>", unsafe_allow_html=True)

# Init message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "🤖 Chào sếp! Tôi là Trình, trợ lý AI của bạn. Hãy bắt đầu trò chuyện nhé!"}
    ]

# Render chat
chat_html = '<div class="chat-box">'
for m in st.session_state.messages:
    role = m["role"]
    content = m["content"]
    if role == "user":
        chat_html += f'<div class="message user">👤 Bạn: {content}</div>'
    elif role == "assistant":
        chat_html += f'<div class="message assistant">🤖: {content}</div>'
    else:
        chat_html += f'<div class="message system">{content}</div>'
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# Input box
user_input = st.text_input("Sếp nhập nội dung cần trao đổi ở đây nhé?", placeholder="Sếp nhập nội dung cần trao đổi ở đây nhé?", label_visibility="collapsed")

# Process input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Đợi Trinh trả lời..."):
        try:
            response = openai.completions.create(
                model="gpt-3.5-turbo",
                # messages=[m for m in st.session_state.messages if m["role"] != "system"]
                prompt="Bạn là một trợ lý AI thông minh. Chào bạn!",  # Tham số prompt
                max_tokens=150  # Số lượng token tối đa (có thể thêm các tham số khác nếu cần)
            )
            reply = response["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.experimental_rerun()
        except Exception as e:
            st.error(f"❌ Lỗi: {e}")
