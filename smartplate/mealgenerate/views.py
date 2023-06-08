from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserInput
import requests

# Create your views here.
from joblib import load

# FPEZq5tfSJQHXCfJwLG7EA==17L22EJwSJ3SbGuC

model = load("./Model/pipelmodel.joblib")


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def calculate_calorie_needs(request):
    if request.method == "POST":
        gender = request.POST["gender"]
        age = request.POST["age"]
        weight = request.POST["weight(kg)"]
        height = request.POST["height(m)"]
        BMI = round(float(weight) / (float(height) ** 2), 1)
        goal = request.POST.get("goal")
        activity_level = request.POST["activity_level"]
        food = request.POST.get("food")

        y_pred = model.predict([[gender, age, weight, height, BMI, activity_level]])

        # Modify the predicted calorie value based on user's goal
        if goal == "lose":
            y_pred *= 0.8
        elif goal == "gain":
            y_pred *= 1.2

        # do something with the input data, e.g. fetch data from the Edamam API

        # create a new UserInput instance and save it to the database
        user_input = UserInput.objects.create(
            gender=gender,
            age=age,
            weight=weight,
            height=height,
            BMI=BMI,
            activity_level=activity_level,
            calorie_needs=round(y_pred[0], 0),
        )

        context = {
            "gender": gender,
            "age": age,
            "weight": weight,
            "height": height,
            "bmi": BMI,
            "activity_level": activity_level,
            "goal": goal,
            "calorie_needs": round(y_pred[0], 0),
            "food": food,
        }
        # return the result to the template
        return render(request, "result.html", context=context)
    return render(request, "main.html")


import requests
from django.shortcuts import render, HttpResponse

import random


def generate_meal(request):
    query = request.GET.get("food")
    calorie_needs = float(request.GET.get("calorie_needs"))

    breakfast_calories = calorie_needs * 0.3
    lunch_calories = calorie_needs * 0.4
    dinner_calories = calorie_needs * 0.3

    breakfast_max_calories = int(breakfast_calories)
    lunch_max_calories = int(lunch_calories)
    dinner_max_calories = int(dinner_calories)

    breakfast_min_calories = int(breakfast_calories * 0.8)
    lunch_min_calories = int(lunch_calories * 0.8)
    dinner_min_calories = int(dinner_calories * 0.8)

    breakfast_data = query_edamam_food_database(
        query, breakfast_min_calories, breakfast_max_calories
    )
    lunch_data = query_edamam_food_database(
        query, lunch_min_calories, lunch_max_calories
    )
    dinner_data = query_edamam_food_database(
        query, dinner_min_calories, dinner_max_calories
    )

    if breakfast_data and lunch_data and dinner_data:
        # Shuffle the meal data to display different meals each time
        random.shuffle(breakfast_data)
        random.shuffle(lunch_data)
        random.shuffle(dinner_data)
        context = {
            "breakfast_data": breakfast_data[0],
            "lunch_data": lunch_data[0],
            "dinner_data": dinner_data[1],
            "calorie_needs": calorie_needs,
        }
        return render(request, "meal_results.html", context)
    else:
        error_message = "Failed to generate meal"
        return HttpResponse(error_message)


def query_edamam_food_database(query, min_calories, max_calories):
    app_id = "46bf6d18"
    app_key = "4379c3ca1500ab593641514b14b8bf9f"
    categoryLabel = "meal"
    url = f"https://api.edamam.com/api/food-database/v2/parser?ingr={query}&categoryLabel={categoryLabel}&app_id={app_id}&app_key={app_key}&nutrition-type=cooking&calories={min_calories}-{max_calories}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()["hints"]
        return data
    else:
        return None
