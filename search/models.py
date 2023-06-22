from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Dish(models.Model):
    id = models.IntegerField(primary_key=True)
    restaurant_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.restaurant_name

