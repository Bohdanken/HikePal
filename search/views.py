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
    if request.method == 'GET':
        user_location = request.GET.get('location')
        trip_dates = request.GET.get('date')

def results_view(request):
    """
    View function for displaying search results.
    """
    return render(request, 'search/results-list-layout-full-page-map.html')
