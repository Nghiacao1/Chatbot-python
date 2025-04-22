import streamlit as st
import openai
import os

# Dùng secrets trong môi trường Streamlit Cloud
openai.api_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY"))

# Cấu hình Streamlit
st.set_page_config(page_title="Trợ lý Em Trinh", page_icon="🧠")
st.title("🧠 Em Trinh - Trợ lý AI")

# Khởi tạo session_state lưu tin nhắn
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Chào bạn! Tôi là Trinh, trợ lý AI của bạn. Hãy bắt đầu trò chuyện nhé!"}
    ]

# Hiển thị các tin nhắn
for msg in st.session_state.messages:
    role = "👤 Bạn" if msg["role"] == "user" else "🤖 Trinh"
    st.markdown(f"**{role}:** {msg['content']}")

# Nhập tin nhắn
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
