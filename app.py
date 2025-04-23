import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Cấu hình API từ secrets
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"  # Bắt buộc cho OpenRouter

# Cấu hình trang
st.set_page_config(page_title="Trợ lý AI", layout="centered")

# Load CSS nếu có
try:
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Header
st.markdown("<h1 class='title'>🧠 Anh Lập Trình - Trợ Lý AI</h1>", unsafe_allow_html=True)

# Khởi tạo lịch sử tin nhắn
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "🤖 Chào sếp! Tôi là Trình, trợ lý AI của bạn. Hãy bắt đầu trò chuyện nhé!"}
    ]

# Hiển thị lịch sử chat
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
user_input = st.text_input("Sếp nhập nội dung cần trao đổi ở đây nhé?", 
                           placeholder="Nhập nội dung...", 
                           label_visibility="collapsed",
                           key="user_input")


# Xử lý đầu vào
if user_input and st.session_state.get("input_submitted", False) is False:
    # Đánh dấu đã xử lý để tránh lặp
    st.session_state.input_submitted = True

    # Lưu tin nhắn người dùng
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

            # Xóa nội dung input và đánh dấu lại để có thể xử lý input mới
            st.session_state.input_box = ""  # reset nội dung input
            st.session_state.input_submitted = False  # cho phép nhập mới
            st.rerun()
        except Exception as e:
            st.error(f"❌ Lỗi: {e}")