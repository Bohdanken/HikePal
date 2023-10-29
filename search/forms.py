from django import forms


class SearchForm(forms.Form):
    city = forms.CharField(max_length=100, min_length=2)
    date = forms.DateField()
