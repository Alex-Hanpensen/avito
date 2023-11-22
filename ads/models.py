from django.db import models


class Ads(models.Model):
    name = models.CharField(max_length=75)
    author = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=19, decimal_places=4)
    description = models.CharField(max_length=5000)
    address = models.CharField(max_length=1024)
    is_published = models.BooleanField()


class Categories(models.Model):
    name = models.CharField(max_length=50)
