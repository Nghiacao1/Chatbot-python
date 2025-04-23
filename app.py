import streamlit as st
import openai
import uuid

# Cấu hình OpenAI
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"

st.set_page_config(page_title="Trợ lý AI", layout="centered")

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

# === Input & xử lý gửi ===
user_input = st.text_input("Nhập nội dung...", 
                           key=st.session_state.input_key,
                           placeholder="Nhập gì đó...", 
                           label_visibility="collapsed")

if user_input:
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
