import re, os
from datetime import datetime
import openai

from django.http import JsonResponse
from django.shortcuts import render, redirect

from chatgpt import transition


def chatbot_view(request):
    """
    View function for displaying chatbot page.
    """
    return render(request, 'search/chat.html')


def chatting_helper(request):
    """
    Helper function for performing chatting
    with the chatbot.
    """
    openai.api_key = os.getenv("chatgpt_api_key")
    message_history = [{"role": "system", "content": "You are a helpful chatbot for answering hiking questions and how we can"
        "take steps towards a more environmentally friendly travel and lifebeing."
        "You can't exit this topic and discuss anything not about the topic under ANY CONDITION"
        "You can provide ideas for trips and hikes based on provided data."
        "Your answers tend to be short unless the user asks to provide detailed answer"}]
    
    if request.method == 'POST':

        user_message = request.POST.get('message')
        message_history.append({"role": "user", "content": user_message})

        reply_content = _send_message_helper(message_history)
        message_history.append({"role": "assistant", "content": reply_content})

        return JsonResponse({'message': reply_content})
    

def _send_message_helper(message):
    """
    Helper function for sending message to ChatGPT.
    """
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message
    )
    reply_content = completion['choices'][0]['message']['content']
    return reply_content


def home_view(request):
    """
    View function for displaying home page.
    """
    return render(request, 'search/index.html')


def search_helper(request):
    """
    Helper function for rendering search request.
    """
    if request.method == 'POST':
        user_location = request.POST.get('popUpLocationInput')
        trip_dates = request.POST.get('popUpDateInput')
        search_radius = request.POST.get('popUpRadiusSelect')
        trip_difficulty = request.POST.get('popUpDifficultSelect')
        equip_present = request.POST.get('popUpEquipRadio')

        print(user_location, trip_dates, search_radius, trip_difficulty, equip_present)
        resulting_dict = _get_search_results_helper(user_location, trip_dates, search_radius, trip_difficulty, equip_present)
        print(resulting_dict)

        context = {
            "resulting_dict": resulting_dict,
            "user_location": user_location.capitalize(),
            "trip_dates": trip_dates,
            "search_radius": search_radius,
            "trip_difficulty": trip_difficulty.capitalize(),
            "equip_present": equip_present,
        }

        return render(request, 'search/results-list-layout-full-page-map.html', context)

    return redirect('/')
    #return render(request, 'search/results-list-layout-full-page-map.html')


def _get_search_results_helper(location, dates, radius, difficulty, equipPresent):
    """
    Helper function for getting search results
    with entered by user parameters.
    """
    day_dates, month_dates = _get_dates_from_dates_string(dates)
    first_date = f"2023-{month_dates[0]}-{day_dates[0]}"
    second_date = f"2023-{month_dates[1]}-{day_dates[1]}"

    resulting_dict = {}
    resulting_dict = transition.get_final_data(first_date, second_date, difficulty, location, radius)

    return resulting_dict


def _get_dates_from_dates_string(date_string):
    """
    Helper function for getting date in optimal format
    from dates string.
    """
    number_pattern = r'\d+'
    month_pattern = r'(?i)(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'

    # Use regular expressions to find all matches
    numbers = re.findall(number_pattern, date_string)
    months = re.findall(month_pattern, date_string)

    # Convert month names to their corresponding month numbers
    month_numbers = [datetime.strptime(month, '%b').month for month in months]

    return numbers, month_numbers
