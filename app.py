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

# Xoá input nếu cần reset
if st.session_state.get("reset_input", False):
    st.session_state.pop("temp_input", None)
    st.session_state["reset_input"] = False

# Khởi tạo lịch sử tin nhắn
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "🤖 Chào sếp! Tôi là Trình, trợ lý AI của bạn. Hãy bắt đầu trò chuyện nhé!"}
    ]

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

# Hiển thị input box
user_input = st.text_input("Sếp nhập nội dung cần trao đổi ở đây nhé?",
                           placeholder="Nhập nội dung...",
                           label_visibility="collapsed",
                           key="temp_input")

# Kiểm tra nếu có nội dung mới
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

            # Cập nhật và trigger reset
            st.session_state.last_input = user_input
            st.session_state["reset_input"] = True
            st.rerun()

        except Exception as e:
            st.error(f"❌ Lỗi: {e}")





