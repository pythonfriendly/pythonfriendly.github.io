from flask import Flask, render_template, request, jsonify
import openai
import os
from textblob import TextBlob

app = Flask(__name__)

# Load API key from environment (Render will store it securely)
openai.api_key = os.getenv("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")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message")

    # Analyze mood using TextBlob
    sentiment = TextBlob(user_message).sentiment.polarity
    if sentiment > 0.3:
        mood = "😊 Positive"
    elif sentiment < -0.3:
        mood = "😔 Negative"
    else:
        mood = "😐 Neutral"

    # AI response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are SAATHI, a friendly Indian youth mental wellness companion."},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response["choices"][0]["message"]["content"]
    return jsonify({"reply": reply, "mood": mood})

if __name__ == "__main__":
    app.run(debug=True)
