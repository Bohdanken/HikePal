from django.http import JsonResponse
from django.shortcuts import render


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

        return render(request, 'search/results-list-layout-full-page-map.html')
