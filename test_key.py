import streamlit as st
import openai

# Sử dụng OpenRouter API
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"

st.title("🔐 Kiểm tra OpenRouter API Key")

if st.button("Gửi yêu cầu test"):
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Chào bạn, bạn có đang hoạt động không?"}],
            max_tokens=50
        )
        reply = response["choices"][0]["message"]["content"]
        st.success(f"✅ Key HOẠT ĐỘNG! Phản hồi từ model:\n\n{reply}")
    except Exception as e:
        st.error(f"❌ Key lỗi hoặc hết hạn: {e}")
