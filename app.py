import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Tải biến môi trường từ tệp .env
load_dotenv()

# Lấy khóa API từ biến môi trường
openai.api_key = os.getenv("OPENROUTER_API_KEY")  # Sử dụng OpenRouter API key nếu bạn dùng OpenRouter

# Kiểm tra xem có API key không
if openai.api_key is None:
    raise ValueError("API Key chưa được thiết lập! Vui lòng thêm OPENROUTER_API_KEY vào tệp .env.")

# Cài đặt cấu hình trang Streamlit
st.set_page_config(page_title="Chatbot AI", layout="centered")

# Hiển thị tiêu đề
st.markdown("# 🧠 Chatbot AI")

# Khởi tạo lịch sử trò chuyện
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Chào bạn! Tôi là Trợ lý AI, bạn cần giúp gì?"}
    ]

# Hiển thị các tin nhắn trong cuộc trò chuyện
chat_html = '<div class="chat-box">'
for m in st.session_state.messages:
    role = m["role"]
    content = m["content"]
    if role == "user":
        chat_html += f'<div class="message user">👤 Bạn: {content}</div>'
    elif role == "assistant":
        chat_html += f'<div class="message assistant">🤖 Trợ lý: {content}</div>'
    else:
        chat_html += f'<div class="message system">{content}</div>'
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# Nhập văn bản của người dùng
user_input = st.text_input("Nhập câu hỏi của bạn:")

# Xử lý đầu vào từ người dùng
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("Đang chờ câu trả lời..."):
        try:
            # Gửi yêu cầu đến OpenAI (hoặc OpenRouter)
            response = openai.completions.create(
                model="gpt-3.5-turbo",  # Hoặc model của OpenRouter
                prompt=user_input,
                max_tokens=150
            )
            reply = response["choices"][0]["text"].strip()
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.experimental_rerun()
        except Exception as e:
            st.error(f"❌ Lỗi: {e}")
