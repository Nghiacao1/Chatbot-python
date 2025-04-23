import streamlit as st
import openai

# Cấu hình OpenAI
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"

st.set_page_config(page_title="Trợ lý AI", layout="centered")

# ===== INIT STATE =====
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "🤖 Chào sếp! Tôi là Trình, trợ lý AI của bạn. Hãy bắt đầu trò chuyện nhé!"}
    ]

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

# ===== XỬ LÝ GỬI (nếu có input mới) =====
if "temp_input" in st.session_state:
    input_val = st.session_state.temp_input.strip()
    if input_val and input_val != st.session_state.last_input:
        st.session_state.messages.append({"role": "user", "content": input_val})
        st.session_state.last_input = input_val

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

        # CLEAR input trước khi render lại
        del st.session_state["temp_input"]
        st.experimental_rerun()

# ===== HIỂN THỊ CHAT =====
st.markdown("<h1 class='title'>🧠 Anh Lập Trình - Trợ Lý AI</h1>", unsafe_allow_html=True)

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

# ===== RENDER INPUT CUỐI CÙNG =====
st.text_input("Nhập nội dung...", key="temp_input", placeholder="Nhập gì đó...", label_visibility="collapsed")
