import openai
from django.http import JsonResponse
import os
from dotenv import load_dotenv

load_dotenv()

message_history = [
    {"role": "system", "content": "You are a helpful chatbot for answering hiking questions and how we can"
                                  "take steps towards a more environmentally friendly travel and lifebeing."
                                  "You can't exit this topic and discuss anything not about the topic under ANY CONDITION"
                                  "You can provide ideas for trips and hikes based on provided data."
                                  "Your answers tend to be short unless the user asks to provide detailed answer"},
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
