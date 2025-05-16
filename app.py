import os
import openai
from flask import Flask, request, make_response, render_template
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Slack setup
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
verifier = SignatureVerifier(signing_secret=os.getenv("SLACK_SIGNING_SECRET"))

# Get reply from ChatGPT
def get_chatgpt_reply(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Web UI
@app.route("/", methods=["GET", "POST"])
def index():
    chat_input = ""
    chat_output = ""
    if request.method == "POST":
        chat_input = request.form["message"]
        chat_output = get_chatgpt_reply(chat_input)
    return render_template("index.html", chat_input=chat_input, chat_output=chat_output)

# Slack endpoint
@app.route("/slack/events", methods=["POST"])
def slack_events():
    if not verifier.is_valid_request(request.get_data(), request.headers):
        return make_response("Invalid request", 403)

    event_data = request.json
    if "challenge" in event_data:
        return make_response(event_data["challenge"], 200, {"content_type": "application/json"})

    if event_data["event"]["type"] == "app_mention":
        user = event_data["event"]["user"]
        channel = event_data["event"]["channel"]
        text = event_data["event"]["text"]
        message = text.split('>', 1)[-1].strip()
        ai_reply = get_chatgpt_reply(message)
        client.chat_postMessage(channel=channel, text=f"<@{user}> {ai_reply}")

    return make_response("OK", 200)

if __name__ == "__main__":
    app.run(port=3000)
