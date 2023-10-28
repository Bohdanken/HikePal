from django.shortcuts import render
from . import forms

def home_view(request):
    return render(request, 'search/index.html')

def results_view(request):
    return render(request, 'search/results-list-layout-full-page-map.html')

def search_view(request):
    form = forms.SearchForm(request.POST)

    if form.is_valid():
        print(form.cleaned_data['city'], form.cleaned_data['date'])

    # execute ChatGPT API request, parse data, and return results page
    context={}  # parsed data with results here
    return render(request, 'search/results-list-layout-full-page-map.html', context=context)
