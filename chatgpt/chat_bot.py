import openai
from django.http import JsonResponse
import os
from dotenv import load_dotenv

load_dotenv()

message_history = [
    {"role": "system", "content": "You are a helpful assistant for answering hiking questions"},
]

def send_message(message_history):
    openai.api_key = os.getenv("chatgpt_api_key")
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=message_history
    )
    reply_content = completion['choices'][0]['message']['content']
    return reply_content

def chat(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        message_history.append({"role": "user", "content": user_message})

        reply_content = send_message(message_history)
        message_history.append({"role": "assistant", "content": reply_content})

        return JsonResponse({'message': reply_content})
def main():
    print("ChatGPT-4 Assistant. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = send_message(user_input)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main()
