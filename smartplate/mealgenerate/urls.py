from django.urls import path
from .views import calculate_calorie_needs, generate_meal, about, home

urlpatterns = [
    path("", home, name="home"),
    path("predict/", calculate_calorie_needs, name="predict"),
    path("generate_meal/", generate_meal, name="generate_meal"),
    path("about/", about, name="about"),
]
