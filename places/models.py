from django.db import models


class Place(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    description_short = models.TextField('Короткое описание')
    description_long = models.TextField('Длинное описание')
    coordinate_lng = models.FloatField('Долгота')
    coordinate_lat = models.FloatField('Широта')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'

