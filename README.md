# AI Automation Slack Bot 🤖

This is a Slack bot built using Python, Flask, Slack API, and OpenAI's ChatGPT. It listens for mentions in Slack and replies with intelligent responses using GPT-3.5.


## Features
- Responds to messages using ChatGPT
- Flask backend with Slack Events API
- Secure API handling via `.env`

## How to Run
1. Create a `.env` file with your API keys
2. Run the server: `python app.py`
3. Start `ngrok`: `ngrok http 3000`

## 🔐 Environment Variables (.env)
- SLACK_BOT_TOKEN=your-slack-bot-token
- SLACK_SIGNING_SECRET=your-signing-secret
- OPENAI_API_KEY=your-openai-api-key

## Future Plans
- Auto workflows
- Task reminders
- Scheduled messages
