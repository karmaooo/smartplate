from django.db import models

# Create your models here.


class UserInput(models.Model):
    gender = models.IntegerField(choices=((1, "Male"), (0, "Female")))
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    BMI = models.FloatField()
    activity_level = models.FloatField(
        choices=(
            (1.2, "Sedentary"),
            (1.3, "Lightly Active"),
            (1.5, "Moderately Active"),
            (1.7, "Very Active"),
            (1.9, "Extremely Active"),
        )
    )

    calorie_needs = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
