import openai
from django.http import JsonResponse
from django.shortcuts import render

message_history = [
    {"role": "system", "content": "You are a helpful assistant for answering hiking questions"},
]


def send_message(message_history):
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
