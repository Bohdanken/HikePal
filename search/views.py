import re
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect

from chatgpt import transition

# ADD LIMIT FOR DATE, UP TO 10 DAYS FROM CURRENT DATE.

def chatbot_view(request):
    return render(request, 'search/chat.html')

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
        user_location = request.POST.get('location')
        trip_dates = request.POST.get('dates')
        search_radius = request.POST.get('radius')
        trip_difficulty = request.POST.get('difficulty')
        equip_present = request.POST.get('equipPresent')

        print(user_location, trip_dates, search_radius, trip_difficulty, equip_present)
        resulting_dict = _get_search_results_helper(user_location, trip_dates, search_radius, trip_difficulty, equip_present)
        print(resulting_dict)

        context = {
            "resulting_dict": resulting_dict,
        }

        return render(request, 'search/results-list-layout-full-page-map.html', context)

    return redirect('/')


def _get_search_results_helper(location, dates, radius, difficulty, equipPresent):
    """
    Helper function for getting search results
    with entered by user parameters.
    """
    day_dates, month_dates = _get_dates_from_dates_string(dates)
    first_date = f"{day_dates[0]}.{month_dates[0]}"
    second_date = f"{day_dates[0]}.{month_dates[0]}"

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
