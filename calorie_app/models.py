from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FoodItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.calories} calories)"
