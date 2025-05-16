import os
import openai
from flask import Flask, request, make_response
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")  # Sets the API key
app = Flask(__name__)

# Setup Slack client and verifier
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
verifier = SignatureVerifier(signing_secret=os.getenv("SLACK_SIGNING_SECRET"))

def get_chatgpt_reply(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return reply.strip()
    except Exception as e:
        return f"Error: {str(e)}"

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

        # Remove the bot mention from text
        message = text.split('>', 1)[-1].strip()

        # Get ChatGPT reply
        ai_reply = get_chatgpt_reply(message)

        client.chat_postMessage(channel=channel, text=f"<@{user}> {ai_reply}")

    return make_response("OK", 200)

if __name__ == "__main__":
    app.run(port=3000)
