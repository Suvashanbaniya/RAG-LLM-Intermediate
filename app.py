from flask import Flask, request, jsonify
from flask_cors import CORS
from pro import ask_llm

app = Flask(__name__)

CORS(app)

@app.route("/")
def home():
    return "Flask is running"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data["message"]

    reply = ask_llm(user_message)

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)