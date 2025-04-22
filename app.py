import streamlit as st
import openai
import os

# Tải CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Tải template
def load_template(chat_html):
    with open("templates/index.html", "r") as f:
        html_template = f.read()
        return html_template.replace("{{ chat_messages }}", chat_html)

# Dùng API key từ Streamlit Secrets
openai.api_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY"))

# Khởi tạo session_state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Chào bạn! Tôi là Trinh, trợ lý AI của bạn. Hãy bắt đầu trò chuyện nhé!"}
    ]

# Tạo HTML từ message
chat_html = ""
for msg in st.session_state.messages:
    role = "👤 Bạn" if msg["role"] == "user" else "🤖 Trinh"
    chat_html += f"<p><strong>{role}:</strong> {msg['content']}</p>"

# Render HTML UI
st.markdown(load_template(chat_html), unsafe_allow_html=True)

# Input box
user_input = st.text_input("Sếp nhập nội dung cần trao đổi ở đây nhé:", key="input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Trinh đang trả lời..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Đã có lỗi xảy ra: {e}")
