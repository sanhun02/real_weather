from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_weather, name='main_weather'),
    path('delete/<city>/', views.delete_from_watchlist, name='delete_from_watchlist'),
    path('detailed/<city>/', views.go_to_detailed_weather, name='go_to_detailed_weather'),
]