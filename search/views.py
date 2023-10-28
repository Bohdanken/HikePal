from django.shortcuts import render

def home_view(request):
    return render(request, 'search/index.html')

def results_view(request):
    return render(request, 'search/results-list-layout-full-page-map.html')
