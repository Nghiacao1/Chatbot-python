import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Cấu hình API
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"

st.set_page_config(page_title="Trợ lý AI", layout="centered")

# ======== RESET INPUT SỚM TRƯỚC KHI RENDER =========
if st.session_state.get("reset_input", False):
    st.session_state.pop("temp_input", None)  # xóa input key
    st.session_state["reset_input"] = False
    st.rerun()  # rerun lại, input sẽ được khởi tạo mới tinh


# ======== KHỞI TẠO BIẾN =========
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "🤖 Chào sếp! Tôi là Trình, trợ lý AI của bạn. Hãy bắt đầu trò chuyện nhé!"}
    ]

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

# ======== Load CSS =========
try:
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# ======== Header =========
st.markdown("<h1 class='title'>🧠 Anh Lập Trình - Trợ Lý AI</h1>", unsafe_allow_html=True)

# ======== Hiển thị chat =========
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

# ======== Input =========
user_input = st.text_input("Sếp nhập nội dung cần trao đổi ở đây nhé?",
                           placeholder="Nhập nội dung...",
                           label_visibility="collapsed",
                           key="temp_input")

# ======== Xử lý gửi =========
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

            # Sau khi nhận được phản hồi:
            # st.session_state.last_input = user_input
            st.session_state.reset_input = True
            user_input = st.text_input("Sếp nhập nội dung cần trao đổi ở đây nhé?",
                           placeholder="Nhập nội dung...",
                           label_visibility="collapsed",
                           key="temp_input")
            st.rerun()  # rerun để trigger đoạn xử lý ở đầu -> xóa input

        except Exception as e:
            st.error(f"❌ Lỗi: {e}")







