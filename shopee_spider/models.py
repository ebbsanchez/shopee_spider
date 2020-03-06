from django.db import models
from django.utils import timezone
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Item(models.Model):
    itemid = models.CharField(max_length=20)
    shopid = models.CharField(max_length=20, default="")
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50, default=None, null=True)
    item_status = models.CharField(max_length=20)

    image = models.CharField(max_length=50)
    images = models.CharField(max_length=500)
    price = models.IntegerField(null=True)
    price_min = models.IntegerField(null=True)
    price_max = models.IntegerField(null=True)
    currency = models.CharField(max_length=10)
    stock = models.IntegerField(null=True)

    view_count = models.IntegerField(null=True)
    liked_count = models.IntegerField(null=True)

    url = models.CharField(max_length=200, default="")

    tag = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL)
    following = models.BooleanField(default=False)
    abandoned = models.BooleanField(default=False)
    updated = models.BooleanField(default=False)

    created = models.DateTimeField(editable=False, default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-modified',)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
