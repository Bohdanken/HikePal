import openai
from django.http import JsonResponse
import os
from dotenv import load_dotenv

load_dotenv()

message_history = [
    {"role": "system", "content": "You are a helpful assistant for answering hiking questions. "
                                  "You can't exit from this topic and discuss anything not about"},
]

def send_message(message):
    openai.api_key = os.getenv("chatgpt_api_key")
    message_history.append({"role": "user", "content": message})
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=message_history
    )
    reply_content = completion['choices'][0]['message']['content']
    return reply_content

def chat():
    print("ChatGPT-4 Assistant. Type 'quit' to exit.")
    while True:
        user_input = "Input"
        if user_input.lower() == 'quit':
            break
        response = send_message(user_input)
        return user_input, f"Assistant: {response}"

if __name__ == "__main__":
    chat()
