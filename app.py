import streamlit as st
import openai
import os

# Load style
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .container { max-width: 700px; margin: auto; padding: 20px; }
        .title { font-size: 32px; font-weight: 600; margin-bottom: 20px; }
        .chat-box { background-color: #f1f1f1; padding: 15px; border-radius: 10px; min-height: 300px; }
        .message { margin-bottom: 10px; }
        .user { text-align: right; color: #1e88e5; }
        .assistant { text-align: left; color: #43a047; }
        .system { font-style: italic; text-align: center; color: #666; }
        .input-form input { width: 100%; padding: 10px; margin-top: 15px; border-radius: 5px; border: 1px solid #ccc; }
    </style>
""", unsafe_allow_html=True)

# Config
openai.api_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY"))
st.markdown('<div class="container"><h1 class="title">🧠 Anh Lập Trình - Trợ Lý AI</h1>', unsafe_allow_html=True)

# State init
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "🤖 Chào sếp! Tôi là Trình, trợ lý AI của bạn. Hãy bắt đầu trò chuyện nhé!"}]

# Render chat messages
chat_html = '<div class="chat-box">'
for msg in st.session_state.messages:
    if msg["role"] == "system":
        chat_html += f'<div class="message system">{msg["content"]}</div>'
    elif msg["role"] == "user":
        chat_html += f'<div class="message user">👤 Bạn: {msg["content"]}</div>'
    else:
        chat_html += f'<div class="message assistant">🤖: {msg["content"]}</div>'
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# Input
user_input = st.text_input("Sếp nhập nội dung cần trao đổi ở đây nhé?", key="chat_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Trinh đang trả lời..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[msg for msg in st.session_state.messages if msg["role"] != "system"]
            )
            reply = response["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Đã có lỗi xảy ra: {e}")

st.markdown('</div>', unsafe_allow_html=True)  # đóng .container
