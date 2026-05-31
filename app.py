from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

llm_url = "http://localhost:11434/api/generate"


def ask_llm(user_input):
    response = requests.post(llm_url, json={
        "model": "llama3",
        "prompt": user_input,
        "stream": False
    })

    data = response.json()
    return data["response"]


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    reply = ask_llm(user_message)

    return jsonify({
        "response": reply
    })


if __name__ == "__main__":
    app.run(debug=True)