from django.db import models


class Place(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    description_short = models.TextField('Короткое описание')
    description_long = models.TextField('Длинное описание')
    lng = models.FloatField('Долгота')
    lat = models.FloatField('Широта')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'


class Image(models.Model):
    number = models.IntegerField('Порядковый номер', default=1,
                                 null=True, blank=True)
    img = models.ImageField('Картинка', upload_to='places_img')
    place = models.ForeignKey('Place', on_delete=models.CASCADE,
                              related_name='images',
                              verbose_name='Место')

    def __str__(self):
        return f'{self.number} {self.place.title}'

    class Meta:
        ordering = ['place__title', 'number']
        verbose_name = 'картинка'
        verbose_name_plural = 'картинки'
