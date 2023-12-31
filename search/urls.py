from django.urls import path, include
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.home_view),
    path('results/', views.search_helper),
    path('ask/', views.chatbot_view),
    path('chat/', views.chatting_helper),
]