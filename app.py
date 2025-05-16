import os
from flask import Flask, request, make_response
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Setup Slack client and verifier
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
verifier = SignatureVerifier(signing_secret=os.getenv("SLACK_SIGNING_SECRET"))

@app.route("/slack/events", methods=["POST"])
def slack_events():
    # Verify that the request is from Slack
    if not verifier.is_valid_request(request.get_data(), request.headers):
        return make_response("Invalid request", 403)

    event_data = request.json

    # Slack sends a challenge when verifying the endpoint
    if "challenge" in event_data:
        return make_response(event_data["challenge"], 200, {"content_type": "application/json"})

    # Respond to messages where the bot is mentioned
    if event_data["event"]["type"] == "app_mention":
        user = event_data["event"]["user"]
        channel = event_data["event"]["channel"]
        text = event_data["event"]["text"]

        response = f"👋 Hi <@{user}>! You said: {text}"
        client.chat_postMessage(channel=channel, text=response)

    return make_response("OK", 200)

if __name__ == "__main__":
    app.run(port=3000)
