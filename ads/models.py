from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Location(models.Model):
    name = models.CharField(max_length=50)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return f'{self.name}'


class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    age = models.IntegerField()
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Ads(models.Model):
    name = models.CharField(max_length=75)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=19, decimal_places=4)
    description = models.CharField(max_length=5000)
    is_published = models.BooleanField()
    image = models.ImageField(upload_to='images/')
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявлении'

    def __str__(self):
        return f'{self.name}'
