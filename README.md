
# EchoMe: AI-Powered Personal Chatbot

**EchoMe** is an AI-driven personal chatbot built with Python, Gradio, and OpenAI. It engages website visitors, answers career-related questions, captures leads via email, and records unknown queries for follow-up. Designed to run efficiently on Hugging Face Spaces, it supports real-time user interaction and backend tool-based actions.

## Live Demo
[Try EchoMe Live] (https://huggingface.co/spaces/bnsnekkanti/EchoMe)

---

## Features

- Answers career and job-related questions using OpenAI’s GPT models
- Collects leads with optional email notifications
- Records unknown queries for future improvement
- Built-in tools for PDF and Markdown processing
- Deployable to [Hugging Face Spaces](https://huggingface.co/spaces)
- Supports real-time interaction using Gradio

---

## 🚀 Development Setup

### Option 1: Using [uv](https://github.com/astral-sh/uv) (Recommended)
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone <your-repo-url>
cd EchoMe

# Create virtual environment and install dependencies
uv venv
uv sync

# Run the application
uv run python app.py


### Option 2: Using pip + venv (Standard)
# Clone the repository
git clone <your-repo-url>
cd EchoMe

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py


### Environment Variables
Create a .env file in the root of your project with the following:
OPENAI_API_KEY=your_openai_api_key

# Email settings (optional, for lead notifications)
EMAIL_SENDER=you@example.com
EMAIL_PASSWORD=your_email_password_or_app_password
EMAIL_RECEIVER=destination@example.com
#Hugging faces settings (optional, for deploying)
HF_TOKEN=your_huging_faces_token # hugging faces token


## 📦 Dependencies
This project uses Python 3.12 and includes dependencies for:

gradio – Web UI framework

openai – GPT model integration

pypdf – PDF parsing

mdurl – Markdown support

smtplib – Email notifications

python-dotenv (optional but recommended)

For the complete list of dependencies, see `requirements.txt`.

