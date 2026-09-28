# imports

from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr
from pydantic import BaseModel

class Evaluation(BaseModel):
    # Indicates if the generated answer meets the required standards
    is_acceptable: bool

    # Provides detailed feedback or reasons why the answer passed or failed
    feedback: str

# Tip: If you're unsure what any of these libraries do,
# Verify that the API key is loaded correctly.
# If you're using a different provider, replace with the appropriate environment variable.
# Note: Ollama does not require an API key.
load_dotenv(override=True)
import os
gemini_api_key = os.getenv('GEMINI_API_KEY')

# if openai_api_key:
#     print(f"OpenAI API Key detected, starting with: {openai_api_key[:8]}...")
# else:
#     print("OpenAI API Key is missing. Please refer to the troubleshooting guide in the setup folder.")

if gemini_api_key:
    print(f"GEMINI API Key detected, starting with: {gemini_api_key[:8]}...")
else:
    print("GEMINI API Key is missing. Please refer to the troubleshooting guide in the setup folder.")


openai = OpenAI(
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/',
    api_key=gemini_api_key
)
model_name = 'gemini-2.0-flash'

# For pushover

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

def push(message):
    print(f"Push: {message}")
    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    requests.post(pushover_url, data=payload)

push("HEY!!")

def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
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


# This function can take a list of tool calls, and run them. This is the IF statement!!

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)

        # THE BIG IF STATEMENT!!!

        if tool_name == "record_user_details":
            result = record_user_details(**arguments)
        elif tool_name == "record_unknown_question":
            result = record_unknown_question(**arguments)

        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results

globals()["record_unknown_question"]("this is a really hard question")

# This is a more elegant way that avoids the IF statement.

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results

reader = PdfReader("me/Profile.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

with open("me/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

name = "Revanth Reddy T"


evaluator_system_prompt = f"You are an evaluator that decides whether a response to a question is acceptable. "\
"You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. "\
"The Agent is playing the role of {name} and is representing {name} on their website. "\
"The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. "\
"The Agent has been provided with context on {name} in the form of their summary and LinkedIn details. Here's the information:"

evaluator_system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"

evaluator_system_prompt += (
    "Evaluate STRICTLY using this rubric. The response is ACCEPTABLE only if ALL are true:\n"
    "1) No raw PII (emails, phone numbers, addresses, SSNs, card numbers, credentials) is echoed back; any such content is redacted with clear placeholders.\n"
    "2) Includes a brief safety disclaimer about not processing or storing sensitive data in this channel.\n"
    "3) Provides secure next-step guidance (e.g., share via a secure portal or remove sensitive details), without requesting more sensitive data.\n"
    "4) Avoids legal/contractual promises; uses neutral, helpful language.\n"
    "5) Addresses the user's intent with helpful, non-sensitive guidance.\n"
    "If any item is missing or violated, set is_acceptable=false and provide precise feedback telling what to fix."
)

def evaluator_user_prompt(reply, message, history):
    user_prompt = f"Here's the conversation between the User and the Agent: \n\n{history}\n\n"
    user_prompt += f"Here's the latest message from the User: \n\n{message}\n\n"
    user_prompt += f"Here's the latest response from the Agent: \n\n{reply}\n\n"
    user_prompt += "Please evaluate the response, replying with whether it is acceptable and your feedback."
    return user_prompt

def evaluate(reply, message, history) -> Evaluation:
    messages = [{"role": "system", "content": evaluator_system_prompt}] + [{"role": "user", "content": evaluator_user_prompt(reply, message, history)}]
    response = openai.beta.chat.completions.parse(model=model_name, messages=messages, response_format=Evaluation)
    return response.choices[0].message.parsed

import re

def contains_sensitive_content(text: str) -> bool:
    if not text:
        return False
    patterns = [
        r"\b\d{3}[- ]?\d{2}[- ]?\d{4}\b",  # SSN-like
        r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b",  # phone
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",  # email
        r"\b\d{13,16}\b",  # potential card number (simplified)
        r"\b(?:cvv|cvc|otp|one[-\s]?time|password|passcode|secret|token)\b",
        r"\b(?:ssn|social security|aadhaar|pan|passport|driver'?s? license)\b",
        r"\b(?:confidential|nda|non[-\s]?disclosure|private|sensitive)\b",
        r"\b(?:address|home address|billing address|shipping address)\b",
        r"\b(?:api key|access key|secret key)\b",
    ]
    for p in patterns:
        if re.search(p, text, flags=re.IGNORECASE):
            return True
    return False

COMPLIANCE_ADDENDUM = (
    "Compliance mode: If the user's message includes personal, confidential, or credential-like data, "
    "you must avoid echoing raw sensitive content. Redact with placeholders like [REDACTED: email] or "
    "[REDACTED: phone]. Include a brief safety disclaimer. Offer secure next steps (e.g., 'Please share via our "
    "secure channel or remove sensitive details'). Provide helpful general guidance without storing or requesting "
    "more sensitive data. Do not make legal promises; use neutral language."
)

system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."


def chat(message, history):
    push(f"New message from user: {message}")
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    done = False
    while not done:

        # This is the call to the LLM - see that we pass in the tools json

        response = openai.chat.completions.create(model=model_name, messages=messages, tools=tools)

        finish_reason = response.choices[0].finish_reason

        # If the LLM wants to call a tool, we do that!

        if finish_reason=="tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True
    return response.choices[0].message.content

def rerun(reply, message, history, feedback):
    updated_system_prompt = system_prompt + "\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
    updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
    updated_system_prompt += f"## Reason for rejection:\n{feedback}\n\n"
    if contains_sensitive_content(message):
        updated_system_prompt += "\n" + COMPLIANCE_ADDENDUM + "\n"
    messages = [{"role": "system", "content": updated_system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=model_name, messages=messages)
    return response.choices[0].message.content

gr.ChatInterface(chat, type="messages").launch()