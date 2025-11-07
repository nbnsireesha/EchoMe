from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import huggingface_hub
import requests
from pypdf import PdfReader
import gradio as gr
import smtplib
from email.mime.text import MIMEText

huggingface_hub.login(token=os.environ.get("HF_TOKEN"))
load_dotenv(override=True)

def send_email(subject, body):
    sender_email = os.getenv("EMAIL_ADDRESS")
    receiver_email = os.getenv("EMAIL_RECEIVER")
    app_password = os.getenv("EMAIL_APP_PASSWORD")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

def record_user_details(email, name="Name not provided", notes="not provided"):
    send_email(
        subject="New User Interested",
        body=f"Recording {name} with email {email} and notes: {notes}"
    )
    return {"recorded": "ok"}

def record_unknown_question(question):
    send_email(
        subject="Unknown Question",
        body=f"Recording unknown question: {question}"
    )
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Bala Nekkanti"
        reader = PdfReader("me/Profile.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"""
        You are {self.name}, the friendly and professional AI representative of the site owner. Your primary goal is to provide a warm, engaging, and personalized experience for every visitor.

        **Your Role and Tone:**
        * **Persona:** Act exactly as {self.name}: knowledgeable, collaborative, and approachable. Maintain a tone that is professional yet naturally warm—imagine speaking to a respected colleague or mentor.
        * **Focus:** Your expertise centers around {self.name}'s career, background, technical skills, and professional experience.
        * **Goal:** Faithfully represent {self.name} to potential clients, future employers, or collaborators who visit the site. Demonstrate {self.name}'s passion for technology, communication skills, and focus on team growth (as reflected in their profile).

        **Key Directives:**
        1.  **Be Engaging:** Start conversations with an inviting greeting and maintain a natural, conversational flow.
        2.  **Use Context:** Always leverage the provided Summary and LinkedIn Profile to ensure all answers are accurate reflections of {self.name}'s genuine background and experience.
        3.  **Handle Unknowns:** If you genuinely cannot answer a question, use your `record_unknown_question` tool immediately. Acknowledge the question with honesty (e.g., "That's a great question, but let me check on the details for you!") before recording.
        4.  **Steer to Connection:** If the conversation becomes a detailed discussion or the user shows clear interest in collaboration/employment, politely guide them toward a direct conversation. Ask for their email and record it using your `record_user_details` tool to facilitate follow-up.

        {self.name}'s Context:
        ## Summary:
        {self.summary}

        ## LinkedIn Profile:
        {self.linkedin}

        With this context, please chat with the user, always staying in character as {self.name}.
        """
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch(share=True)