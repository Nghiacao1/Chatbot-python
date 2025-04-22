import streamlit as st
from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

if os.getenv("STREAMLIT_ENV") != "cloud":
    from dotenv import load_dotenv
    load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)

messages = []

@app.route("/", methods=["GET", "POST"])
def index():
    global messages
    if request.method == "POST":
        user_input = request.form["message"]
        messages.append({"role": "user", "content": user_input})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": bot_reply})
    
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
