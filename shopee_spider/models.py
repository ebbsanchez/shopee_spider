from django.db import models

# Create your models here.


class Item(models.Model):
    itemid = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    item_status = models.CharField(max_length=20)
    image = models.CharField(max_length=50)
    images = models.CharField(max_length=500)
    price = models.IntegerField(null=True)
    price_min = models.IntegerField(null=True)
    price_max = models.IntegerField(null=True)
    currency = models.CharField(max_length=10)

    following = models.BooleanField(default=False)
    abandoned = models.BooleanField(default=False)
    updated = models.BooleanField(default=False)

    def __str__(self):
        return self.name
